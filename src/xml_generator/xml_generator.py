import logging
import random
from logging import Logger
from pathlib import Path
from xml.etree.ElementTree import Element as XmlElement, ElementTree as XmlElementTree, indent

from xmlschema import XMLSchema, XMLSchemaValidationError
from xmlschema.validators import (
    XsdAtomicBuiltin,
    XsdAtomicRestriction,
    XsdAttribute,
    XsdComplexType,
    XsdElement,
    XsdFacet,
    XsdFractionDigitsFacet,
    XsdGroup,
    XsdMaxExclusiveFacet,
    XsdMaxInclusiveFacet,
    XsdMaxLengthFacet,
    XsdMinExclusiveFacet,
    XsdMinInclusiveFacet,
    XsdMinLengthFacet,
    XsdPatternFacets,
    XsdSimpleType,
    XsdTotalDigitsFacet,
    XsdWhiteSpaceFacet
)

from xml_generator.tag_decimal_string_generator import TagDecimalStringGenerator
from xml_generator.tag_random_boolean_string_generator import TagRandomBooleanStringGenerator
from xml_generator.tag_random_date_string_generator import TagRandomDateStringGenerator
from xml_generator.tag_random_date_time_string_generator import TagRandomDateTimeStringGenerator
from xml_generator.tag_random_decimal_string_generator import TagRandomDecimalStringGenerator
from xml_generator.tag_random_hexadecimal_binary_string_generator import TagRandomHexadecimalBinaryStringGenerator
from xml_generator.tag_random_integer_string_generator import TagRandomIntegerStringGenerator
from xml_generator.tag_random_string_generator import TagRandomStringGenerator
from xml_generator.tag_random_time_string_generator import TagRandomTimeStringGenerator
from xml_generator.tag_specific_length_random_hexadecimal_binary_string_generator import (
    TagSpecificLengthHexadecimalBinaryStringGenerator
)
from xml_generator.tag_specific_length_string_generator import TagSpecificLengthStringGenerator
from xml_generator.tag_white_space_policy import TagWhiteSpacePolicy


class XmlGenerator:
    _log: Logger = logging.getLogger(__name__)
    _force_min_occurs: bool
    _force_max_occurs: bool
    _force_default_value: bool
    _force_min_value: bool
    _force_max_value: bool
    _tag_decimal_string_generator: TagDecimalStringGenerator
    _tag_random_boolean_string_generator: TagRandomBooleanStringGenerator
    _tag_random_date_string_generator: TagRandomDateStringGenerator
    _tag_random_date_time_string_generator: TagRandomDateTimeStringGenerator
    _tag_random_decimal_string_generator: TagRandomDecimalStringGenerator
    _tag_random_hexadecimal_binary_string_generator: TagRandomHexadecimalBinaryStringGenerator
    _tag_random_integer_string_generator: TagRandomIntegerStringGenerator
    _tag_random_string_generator: TagRandomStringGenerator
    _tag_random_time_string_generator: TagRandomTimeStringGenerator
    _tag_specific_length_random_hexadecimal_binary_string_generator: TagSpecificLengthHexadecimalBinaryStringGenerator
    _tag_specific_length_string_generator: TagSpecificLengthStringGenerator

    def __init__(
        self,
        force_min_occurs: bool = False,
        force_max_occurs: bool = False,
        force_default_value: bool = False,
        force_min_value: bool = False,
        force_max_value: bool = False
    ) -> None:
        self._force_min_occurs = force_min_occurs
        self._force_max_occurs = force_max_occurs
        self._force_default_value = force_default_value
        self._force_min_value = force_min_value
        self._force_max_value = force_max_value
        self._tag_decimal_string_generator = TagDecimalStringGenerator()
        self._tag_random_boolean_string_generator = TagRandomBooleanStringGenerator()
        self._tag_random_date_string_generator = TagRandomDateStringGenerator()
        self._tag_random_date_time_string_generator = TagRandomDateTimeStringGenerator()
        self._tag_random_decimal_string_generator = TagRandomDecimalStringGenerator()
        self._tag_random_hexadecimal_binary_string_generator = TagRandomHexadecimalBinaryStringGenerator()
        self._tag_random_integer_string_generator = TagRandomIntegerStringGenerator()
        self._tag_random_string_generator = TagRandomStringGenerator()
        self._tag_random_time_string_generator = TagRandomTimeStringGenerator()
        self._tag_specific_length_random_hexadecimal_binary_string_generator = (
            TagSpecificLengthHexadecimalBinaryStringGenerator()
        )
        self._tag_specific_length_string_generator = TagSpecificLengthStringGenerator()

    def generate_xml(self, xsd_path: Path, xml_path: Path, root_element_name: str) -> int:
        self._log.info(f'Generating XML for XSD \'{xsd_path}\'...')
        exit_code: int = 1
        try:
            if self._force_min_occurs and self._force_max_occurs:
                raise ValueError('\'force_min_occurs\' and \'force_max_occurs\' parameters cannot be both True')
            if self._force_min_value and self._force_max_value:
                raise ValueError('\'force_min_value\' and \'force_max_value\' parameters cannot be both True')
            if not xsd_path.is_file():
                raise FileNotFoundError(f'XSD file \'{xsd_path}\' does not exist')
            xml_schema: XMLSchema = XMLSchema(xsd_path)
            root_xml_element: XmlElement = self._xsd_element_to_xml_element(xml_schema.elements[root_element_name])
            xml_element_tree: XmlElementTree = XmlElementTree(root_xml_element)
            indent(tree=xml_element_tree, space=(' ' * 4), level=0)
            xml_element_tree.write(file_or_filename=xml_path, encoding='utf-8', xml_declaration=True)
            self._log.info('Validating XML...')
            xml_schema.validate(xml_path)
            self._log.info(f'XML generated successfully at \'{xml_path}\'')
            exit_code = 0
        except XMLSchemaValidationError as exception:
            self._log.error(f'XML validation error: {exception}')
            if xml_path.exists():
                xml_path.unlink()
        except Exception as exception:
            self._log.error(f'Exception found while generating  XML: {exception.__class__.__name__} - {exception}')
        return exit_code

    def _xsd_element_to_xml_element(self, xsd_element: XsdElement) -> XmlElement:
        xml_element: XmlElement
        if xsd_element.fixed is not None:
            self._log.debug(f'Generating fixed element \'{xsd_element.name}\'...')
            xml_element = self._xsd_fixed_element_to_xml_element(xsd_element)
            self._log.debug(f'Fixed element \'{xsd_element.name}\' generated')
        elif xsd_element.type.is_complex():
            self._log.debug(f'Generating complex element \'{xsd_element.name}\'...')
            xml_element = self._xsd_complex_element_to_xml_element(xsd_element)
            xml_element.attrib = self._get_xsd_element_attributes(xsd_element)
            self._log.debug(f'Complex element \'{xsd_element.name}\' generated')
        elif xsd_element.type.is_simple():
            self._log.debug(f'Generating simple element \'{xsd_element.name}\'...')
            xml_element = self._xsd_simple_element_to_xml_element(xsd_element)
            self._log.debug(f'Simple element \'{xsd_element.name}\' generated')
        else:
            raise NotImplementedError(f'Unknown XSD element type {xsd_element.type} for {self}')
        return xml_element

    def _get_xsd_element_attributes(self, xsd_element: XsdElement) -> dict[str, str]:
        attributes: dict[str, str] = {}
        attribute_name: str
        xsd_attribute: XsdAttribute
        for attribute_name, xsd_attribute in xsd_element.attributes.items():
            attributes[attribute_name] = self._get_xsd_simple_tag_value(
                xsd_tag=xsd_attribute.type,
                xsd_tag_default_value=xsd_attribute.default
            )
        return attributes

    @staticmethod
    def _xsd_fixed_element_to_xml_element(xsd_element: XsdElement) -> XmlElement:
        xml_element: XmlElement = XmlElement(xsd_element.name)
        xml_element.text = xsd_element.fixed
        return xml_element

    def _xsd_complex_element_to_xml_element(self, xsd_element: XsdElement) -> XmlElement:
        if isinstance(xsd_element.type.content, XsdGroup):
            return self._xsd_group_element_to_xml_element(xsd_element)
        elif xsd_element.type.is_extension():
            return self._xsd_extension_element_to_xml_element(xsd_element)
        else:
            return self._xsd_simple_element_to_xml_element(xsd_element)

    def _xsd_extension_element_to_xml_element(self, xsd_element: XsdElement) -> XmlElement:
        return self._xsd_element_to_xml_element(xsd_element.type.base_type)
        base_types: list[XsdSimpleType | XsdComplexType] = []
        current_type = xsd_element.type.base_type
        while current_type.base_type is not None:
            base_type = current_type.base_type
            base_types.append(base_type)
            current_type = base_type

        pass

    def _xsd_group_element_to_xml_element(self, xsd_element: XsdElement) -> XmlElement:
        xml_element: XmlElement = XmlElement(xsd_element.name)
        choice_xsd_elements: list[XsdElement] = []
        xsd_child_element: XsdElement
        for xsd_child_element in xsd_element.type.content.iter_elements():
            min_occurs: int = xsd_child_element.min_occurs
            max_occurs: int = 1 if xsd_child_element.max_occurs is None else xsd_child_element.max_occurs
            occurs: int
            if self._force_min_occurs:
                occurs = min_occurs
            elif self._force_max_occurs:
                occurs = max_occurs
            else:
                occurs = random.randint(a=min_occurs, b=max_occurs)
            for _ in range(occurs):
                if xsd_child_element.parent.model == 'choice':
                    choice_xsd_elements.append(xsd_child_element)
                else:
                    if choice_xsd_elements:
                        xml_child_element: XmlElement = self._xsd_element_to_xml_element(
                            random.choice(choice_xsd_elements)
                        )
                        xml_element.append(xml_child_element)
                        choice_xsd_elements = []
                    xml_child_element: XmlElement = self._xsd_element_to_xml_element(xsd_child_element)
                    xml_element.append(xml_child_element)
        if choice_xsd_elements:  # Add remaining choice elements, if any
            xml_child_element: XmlElement = self._xsd_element_to_xml_element(random.choice(choice_xsd_elements))
            xml_element.append(xml_child_element)
        return xml_element

    def _xsd_simple_element_to_xml_element(self, xsd_element: XsdElement) -> XmlElement:
        if xsd_element.type.is_list():
            raise NotImplementedError(f'List type is not implemented by {self}')
        elif xsd_element.type.is_union():
            raise NotImplementedError(f'Union type is not implemented by {self}')
        else:
            xml_element: XmlElement = XmlElement(xsd_element.name)
            xml_element.text = self._get_xsd_simple_tag_value(
                xsd_tag=xsd_element.type,
                xsd_tag_default_value=xsd_element.default
            )
            return xml_element

    def _get_xsd_simple_tag_value(self, xsd_tag: XsdSimpleType, xsd_tag_default_value: str | None) -> str:
        if xsd_tag_default_value and self._force_default_value:
            return xsd_tag_default_value
        elif isinstance(xsd_tag, XsdAtomicBuiltin):
            return self._get_xsd_atomic_builtin_tag_value(xsd_tag)
        elif isinstance(xsd_tag, XsdAtomicRestriction):
            return self._get_xsd_atomic_restriction_tag_value(xsd_tag)
        else:
            raise NotImplementedError(f'Unknown simple tag type {xsd_tag} for {self}')

    def _get_xsd_atomic_builtin_tag_value(self, xsd_tag: XsdAtomicBuiltin) -> str:
        if xsd_tag.local_name == 'time':
            return self._tag_random_time_string_generator.generate_random_time_string_for_tag()
        elif xsd_tag.local_name == 'boolean':
            return self._tag_random_boolean_string_generator.generate_random_boolean_string_for_tag()
        else:
            raise NotImplementedError(f'Unknown atomic built-in tag type: {xsd_tag.local_name}')

    def _get_xsd_atomic_restriction_tag_value(self, xsd_tag: XsdAtomicRestriction) -> str:
        if xsd_tag.enumeration is not None:
            return random.choice(xsd_tag.enumeration)
        elif xsd_tag.base_type.local_name == 'dateTime':
            return self._tag_random_date_time_string_generator.generate_random_date_time_string_for_tag()
        elif xsd_tag.base_type.local_name == 'date':
            return self._tag_random_date_string_generator.generate_random_date_string_for_tag()
        else:
            pattern: str | None = None
            min_length: int | None = None
            max_length: int | None = None
            min_inclusive: float | None = None
            max_inclusive: float | None = None
            min_exclusive: float | None = None
            max_exclusive: float | None = None
            total_digits: int | None = None
            fraction_digits: int | None = None
            white_space_policy: TagWhiteSpacePolicy | None = None

            facet: XsdFacet
            for facet in xsd_tag.facets.values():
                if isinstance(facet, XsdFractionDigitsFacet):
                    fraction_digits = facet.value
                elif isinstance(facet, XsdMaxExclusiveFacet):
                    max_exclusive = float(facet.value)
                elif isinstance(facet, XsdMaxInclusiveFacet):
                    max_inclusive = float(facet.value)
                elif isinstance(facet, XsdMaxLengthFacet):
                    max_length = facet.value
                elif isinstance(facet, XsdMinExclusiveFacet):
                    min_exclusive = float(facet.value)
                elif isinstance(facet, XsdMinInclusiveFacet):
                    min_inclusive = float(facet.value)
                elif isinstance(facet, XsdMinLengthFacet):
                    min_length = int(facet.value)
                elif isinstance(facet, XsdPatternFacets):
                    pattern = facet.regexps[0]
                elif isinstance(facet, XsdTotalDigitsFacet):
                    total_digits = facet.value
                elif isinstance(facet, XsdWhiteSpaceFacet):
                    white_space_policy = TagWhiteSpacePolicy(facet.value)

            xsd_data_type: str | None = xsd_tag.base_type.local_name
            if xsd_data_type == 'string':
                if min_length and self._force_min_value and not pattern:
                    return self._tag_specific_length_string_generator.generate_specific_length_string_for_tag(
                        length=min_length,
                        white_space_policy=white_space_policy
                    )
                elif max_length and self._force_max_value and not pattern:
                    return self._tag_specific_length_string_generator.generate_specific_length_string_for_tag(
                        length=max_length,
                        white_space_policy=white_space_policy
                    )
                else:
                    return self._tag_random_string_generator.generate_random_string_for_tag(
                        tag_name=xsd_tag.parent.name,
                        min_length=min_length,
                        max_length=max_length,
                        pattern=pattern,
                        white_space_policy=white_space_policy
                    )
            elif xsd_data_type == 'integer' or xsd_data_type == 'int' or xsd_data_type == 'long':
                if min_inclusive and self._force_min_value:
                    return str(int(min_inclusive))
                elif max_inclusive and self._force_max_value:
                    return str(int(max_inclusive))
                else:
                    return self._tag_random_integer_string_generator.generate_random_integer_string_for_tag(
                        tag_name=xsd_tag.parent.name,
                        pattern=pattern,
                        min_inclusive=int(min_inclusive) if min_inclusive else min_inclusive,
                        max_inclusive=int(max_inclusive) if max_inclusive else max_inclusive,
                        min_exclusive=int(min_exclusive) if min_exclusive else min_exclusive,
                        max_exclusive=int(max_exclusive) if max_exclusive else max_exclusive,
                        total_digits=total_digits
                    )
            elif xsd_data_type == 'decimal':
                if min_inclusive and self._force_min_value:
                    return self._tag_decimal_string_generator.generate_decimal_string_for_tag(
                        value=min_inclusive,
                        fraction_digits=fraction_digits
                    )
                elif max_inclusive and self._force_max_value:
                    return self._tag_decimal_string_generator.generate_decimal_string_for_tag(
                        value=max_inclusive,
                        fraction_digits=fraction_digits
                    )
                else:
                    return self._tag_random_decimal_string_generator.generate_random_decimal_string_for_tag(
                        tag_name=xsd_tag.parent.name,
                        pattern=pattern,
                        min_inclusive=min_inclusive,
                        max_inclusive=max_inclusive,
                        min_exclusive=min_exclusive,
                        max_exclusive=max_exclusive,
                        fraction_digits=fraction_digits
                    )
            elif xsd_data_type == 'hexBinary':
                if min_length and self._force_min_value:
                    return self._tag_specific_length_random_hexadecimal_binary_string_generator.generate_specific_length_hexadecimal_binary_string_for_tag(
                        min_length
                    )
                elif max_length and self._force_max_value:
                    return self._tag_specific_length_random_hexadecimal_binary_string_generator.generate_specific_length_hexadecimal_binary_string_for_tag(
                        max_length
                    )
                else:
                    return self._tag_random_hexadecimal_binary_string_generator.generate_random_hexadecimal_binary_string_for_tag(
                        min_length=min_length,
                        max_length=max_length
                    )
            else:
                raise NotImplementedError(f'Unsupported data type \'{xsd_data_type}\' by {self}')

    def __str__(self) -> str:
        return self.__class__.__name__
