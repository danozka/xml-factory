import logging
import random
from logging import Logger
from pathlib import Path
from xml.etree.ElementTree import Element, ElementTree, indent

from xmlschema.validators import XMLSchema, XMLSchemaValidationError, XsdAttribute, XsdElement, XsdGroup

from xml_factory.xml_simple_type_value_generator import XmlSimpleTypeValueGenerator


class XmlGenerator:
    _ENCODING: str = 'utf-8'
    _EXIT_CODE_SUCCESS: int  = 0
    _EXIT_CODE_FAILURE: int  = 1
    _INDENT_SPACES: int = 4
    _log: Logger = logging.getLogger(__name__)
    _force_default_value: bool
    _xml_simple_type_value_generator: XmlSimpleTypeValueGenerator

    def __init__(
        self,
        force_default_value: bool = False,
        xml_simple_type_value_generator: XmlSimpleTypeValueGenerator = XmlSimpleTypeValueGenerator()
    ) -> None:
        self._force_default_value = force_default_value
        self._xml_simple_type_value_generator = xml_simple_type_value_generator

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
            xml_element = Element(xsd_element.local_name)
            if xsd_element.fixed is not None:
                xml_element.text = xsd_element.fixed
            elif xsd_element.default is not None and self._force_default_value:
                xml_element.text = xsd_element.default
            else:
                xml_element.text = self._xml_simple_type_value_generator.generate_xml_simple_type_value(
                    xsd_element.type
                )
        else:
            xml_element = self._generate_xml_complex_type_element(xsd_element)
        return xml_element

    def _generate_xml_complex_type_element(self, xsd_element: XsdElement) -> Element:
        xml_element: Element = Element(xsd_element.local_name)
        if xsd_element.type.model_group is not None:
            self._populate_xml_group_element(xml_parent_element=xml_element, xsd_group=xsd_element.type.content)
        else:
            xml_element.text = self._xml_simple_type_value_generator.generate_xml_simple_type_value(
                xsd_element.type.content
            )
        attribute_name: str
        xsd_attribute: XsdAttribute
        for attribute_name, xsd_attribute in xsd_element.attributes.items():
            if xsd_attribute.fixed is not None:
                xml_element.attrib[attribute_name] = xsd_attribute.fixed
            elif xsd_attribute.default is not None and self._force_default_value:
                xml_element.attrib[attribute_name] = xsd_element.default
            else:
                xml_element.attrib[attribute_name] = (
                    self._xml_simple_type_value_generator.generate_xml_simple_type_value(xsd_attribute.type)
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
        if isinstance(group_content, XsdElement):
            xml_parent_element.append(self._generate_xml_element(group_content))
        elif isinstance(group_content, XsdGroup):
            self._populate_xml_group_element(xml_parent_element=xml_parent_element, xsd_group=group_content)
        else:
            raise NotImplementedError(f'Unknown group content {group_content}')
