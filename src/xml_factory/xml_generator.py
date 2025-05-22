import logging
import random
from logging import Logger
from pathlib import Path
from xml.etree.ElementTree import Element, ElementTree, indent

from xmlschema.validators import (
    XMLSchema,
    XMLSchemaValidationError,
    XsdAttribute,
    XsdElement,
    XsdFacet,
    XsdFractionDigitsFacet,
    XsdGroup,
    XsdLengthFacet,
    XsdList,
    XsdMaxExclusiveFacet,
    XsdMaxInclusiveFacet,
    XsdMaxLengthFacet,
    XsdMinExclusiveFacet,
    XsdMinInclusiveFacet,
    XsdMinLengthFacet,
    XsdPatternFacets,
    XsdSimpleType,
    XsdTotalDigitsFacet,
    XsdUnion
)

from xml_factory.complex.i_group_content_number_of_occurrences_getter import IGroupContentNumberOfOccurrencesGetter
from xml_factory.domain.base_type import BaseType
from xml_factory.domain.restriction import Restriction
from xml_factory.simple.i_list_number_of_items_getter import IListNumberOfItemsGetter
from xml_factory.simple.i_restriction_pattern_value_generator import IRestrictionPatternValueGenerator
from xml_factory.simple.i_restriction_value_generator import IRestrictionValueGenerator


class XmlGenerator:
    _ENCODING: str = 'utf-8'
    _EXIT_CODE_SUCCESS: int  = 0
    _EXIT_CODE_FAILURE: int  = 1
    _INDENT_SPACES: int = 2
    _log: Logger = logging.getLogger(__name__)
    _group_content_number_of_occurrences_getter: IGroupContentNumberOfOccurrencesGetter
    _list_number_of_items_getter: IListNumberOfItemsGetter
    _restriction_pattern_value_generator: IRestrictionPatternValueGenerator
    _restriction_value_generator: IRestrictionValueGenerator
    _force_default_value: bool

    def __init__(
        self,
        group_content_number_of_occurrences_getter: IGroupContentNumberOfOccurrencesGetter,
        list_number_of_items_getter: IListNumberOfItemsGetter,
        restriction_pattern_value_generator: IRestrictionPatternValueGenerator,
        restriction_value_generator: IRestrictionValueGenerator,
        force_default_value: bool = False
    ) -> None:
        self._group_content_number_of_occurrences_getter = group_content_number_of_occurrences_getter
        self._list_number_of_items_getter = list_number_of_items_getter
        self._restriction_pattern_value_generator = restriction_pattern_value_generator
        self._restriction_value_generator = restriction_value_generator
        self._force_default_value = force_default_value

    def generate_xml(self, xsd_path: Path, xml_path: Path, root_element_name: str) -> int:
        self._log.info(f'Generating XML for XSD \'{xsd_path}\'...')
        exit_code: int = self._EXIT_CODE_FAILURE
        try:
            if not xsd_path.is_file():
                raise FileNotFoundError(f'XSD file \'{xsd_path}\' does not exist')
            xml_schema: XMLSchema = XMLSchema(xsd_path)
            xml_element_tree: ElementTree = ElementTree(
                self._generate_xml_element(xml_schema.elements[root_element_name])
            )
            indent(tree=xml_element_tree, space=(' ' * self._INDENT_SPACES), level=0)
            xml_element_tree.write(file_or_filename=xml_path, encoding=self._ENCODING, xml_declaration=True)
            self._log.info('Validating XML...')
            xml_schema.validate(xml_path)
            self._restriction_pattern_value_generator.update_patterns()
            self._log.info(f'XML generated successfully at \'{xml_path}\'')
            exit_code = self._EXIT_CODE_SUCCESS
        except XMLSchemaValidationError as exception:
            self._log.error(f'XML validation error: {exception}')
            if xml_path.exists():
                xml_path.unlink()
        except Exception as ex:
            self._log.error(f'Exception found while generating XML: {ex.__class__.__name__} - {ex}')
        return exit_code

    def _generate_xml_element(self, xsd_element: XsdElement) -> Element:
        xml_element: Element
        if xsd_element.type.is_simple():
            self._log.debug(f'Generating simple type element \'{xsd_element.local_name}\'')
            xml_element = Element(xsd_element.local_name)
            if xsd_element.fixed is not None:
                xml_element.text = xsd_element.fixed
            elif xsd_element.default is not None and self._force_default_value:
                xml_element.text = xsd_element.default
            else:
                xml_element.text = self._generate_xml_simple_type_value(
                    element_name=xsd_element.local_name,
                    xsd_simple_type=xsd_element.type
                )
            self._log.debug(f'Simple type element \'{xsd_element.local_name}\' generated successfully')
        else:
            self._log.debug(f'Generating complex type element \'{xsd_element.local_name}\'')
            xml_element = self._generate_xml_complex_type_element(xsd_element)
            self._log.debug(f'Complex type element \'{xsd_element.local_name}\' generated successfully')
        return xml_element

    def _generate_xml_simple_type_value(self, element_name: str, xsd_simple_type: XsdSimpleType) -> str:
        if xsd_simple_type.is_list():
            list_restriction: Restriction = self._get_xml_simple_type_restriction(xsd_simple_type)
            list_number_of_items: int = self._list_number_of_items_getter.get_list_number_of_items(list_restriction)
            current_type: XsdSimpleType = xsd_simple_type
            while not isinstance(current_type, XsdList):
                current_type = current_type.base_type
            xsd_list_item_simple_type: XsdSimpleType = current_type.item_type
            return ' '.join(
                [
                    self._generate_xml_simple_type_value(
                        element_name=element_name,
                        xsd_simple_type=xsd_list_item_simple_type
                    )
                    for _ in range(list_number_of_items)
                ]
            )
        elif xsd_simple_type.is_union():
            xsd_simple_type: XsdUnion
            selected_xsd_simple_type: XsdSimpleType = random.choice(xsd_simple_type.member_types)
            return self._generate_xml_simple_type_value(
                element_name=element_name,
                xsd_simple_type=selected_xsd_simple_type
            )
        else:
            restriction: Restriction = self._get_xml_simple_type_restriction(xsd_simple_type)
            if restriction.enumeration is not None:
                return random.choice(restriction.enumeration)
            elif restriction.pattern is not None:
                return self._restriction_pattern_value_generator.generate_restriction_pattern_value(
                    element_name=element_name,
                    restriction=restriction
                )
            else:
                return self._restriction_value_generator.generate_restriction_value(restriction)

    def _get_xml_simple_type_restriction(self, xsd_simple_type: XsdSimpleType) -> Restriction:
        restriction: Restriction = Restriction()
        current_type: XsdSimpleType = xsd_simple_type
        while current_type.is_restriction():
            self._update_xml_simple_type_restriction_facets(restriction=restriction, xsd_simple_type=current_type)
            current_type = current_type.base_type
        self._update_xml_simple_type_restriction_facets(restriction=restriction, xsd_simple_type=current_type)
        restriction.base_type = BaseType(current_type.python_type)
        return restriction
    
    @staticmethod
    def _update_xml_simple_type_restriction_facets(restriction: Restriction, xsd_simple_type: XsdSimpleType) -> None:
        if restriction.enumeration is None:
            restriction.enumeration = xsd_simple_type.enumeration
        facet: XsdFacet
        for facet in xsd_simple_type.facets.values():
            if isinstance(facet, XsdFractionDigitsFacet):
                if restriction.fraction_digits is None:
                    restriction.fraction_digits = facet.value
            elif isinstance(facet, XsdLengthFacet):
                if restriction.length is None:
                    restriction.length = facet.value
            elif isinstance(facet, XsdMaxExclusiveFacet):
                if restriction.max_exclusive is None:
                    restriction.max_exclusive = facet.value
            elif isinstance(facet, XsdMaxInclusiveFacet):
                if restriction.max_inclusive is None:
                    restriction.max_inclusive = facet.value
            elif isinstance(facet, XsdMaxLengthFacet):
                if restriction.max_length is None:
                    restriction.max_length = facet.value
            elif isinstance(facet, XsdMinExclusiveFacet):
                if restriction.min_exclusive is None:
                    restriction.min_exclusive = facet.value
            elif isinstance(facet, XsdMinInclusiveFacet):
                if restriction.min_inclusive is None:
                    restriction.min_inclusive = facet.value
            elif isinstance(facet, XsdMinLengthFacet):
                if restriction.min_length is None:
                    restriction.min_length = facet.value
            elif isinstance(facet, XsdPatternFacets):
                if restriction.pattern is None:
                    restriction.pattern = random.choice(facet.regexps)
            elif isinstance(facet, XsdTotalDigitsFacet):
                if restriction.total_digits is None:
                    restriction.total_digits = facet.value

    def _generate_xml_complex_type_element(self, xsd_element: XsdElement) -> Element:
        xml_element: Element = Element(xsd_element.local_name)
        if xsd_element.type.model_group is not None:
            xsd_group: XsdGroup = xsd_element.type.content
            number_of_occurrences: int = (
                self._group_content_number_of_occurrences_getter.get_group_content_number_of_occurrences(xsd_group)
            )
            for _ in range(number_of_occurrences):
                self._populate_xml_group_element(xml_parent_element=xml_element, xsd_group=xsd_group)
        else:
            xsd_simple_type: XsdSimpleType = xsd_element.type.content
            xml_element.text = self._generate_xml_simple_type_value(
                element_name=xsd_element.local_name,
                xsd_simple_type=xsd_simple_type
            )
        attribute_name: str
        xsd_attribute: XsdAttribute
        for attribute_name, xsd_attribute in xsd_element.attributes.items():
            if xsd_attribute.fixed is not None:
                xml_element.attrib[attribute_name] = xsd_attribute.fixed
            elif xsd_attribute.default is not None and self._force_default_value:
                xml_element.attrib[attribute_name] = xsd_attribute.default
            else:
                xml_element.attrib[attribute_name] = self._generate_xml_simple_type_value(
                    element_name=attribute_name,
                    xsd_simple_type=xsd_attribute.type
                )
        return xml_element

    def _populate_xml_group_element(self, xml_parent_element: Element, xsd_group: XsdGroup) -> None:
        group_content: XsdElement | XsdGroup
        if xsd_group.model == 'all':
            random.shuffle(xsd_group.content)
            for group_content in xsd_group.content:
                self._handle_group_content(xml_parent_element=xml_parent_element, group_content=group_content)
        elif xsd_group.model == 'choice':
            group_content = random.choice(xsd_group.content)
            self._handle_group_content(xml_parent_element=xml_parent_element, group_content=group_content)
        elif xsd_group.model == 'sequence':
            for group_content in xsd_group.content:
                self._handle_group_content(xml_parent_element=xml_parent_element, group_content=group_content)
        else:
            raise NotImplementedError(f'Unknown group model \'{xsd_group.model}\'')

    def _handle_group_content(self, xml_parent_element: Element, group_content: XsdElement | XsdGroup) -> None:
        number_of_occurrences: int = (
            self._group_content_number_of_occurrences_getter.get_group_content_number_of_occurrences(group_content)
        )
        for _ in range(number_of_occurrences):
            if isinstance(group_content, XsdElement):
                xml_parent_element.append(self._generate_xml_element(group_content))
            elif isinstance(group_content, XsdGroup):
                self._populate_xml_group_element(xml_parent_element=xml_parent_element, xsd_group=group_content)
            else:
                raise NotImplementedError(f'Unknown group content {group_content}')
