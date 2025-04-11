import logging
import random
from logging import Logger
from pathlib import Path
from xml.etree.ElementTree import Element, ElementTree, indent

from xmlschema.validators import XMLSchema, XMLSchemaValidationError, XsdAttribute, XsdElement, XsdGroup, XsdSimpleType
from xml_factory.xml_simple_type_value_generator import XmlSimpleTypeValueGenerator


class XmlGenerator:
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
        exit_code: int = 1
        try:
            if not xsd_path.is_file():
                raise FileNotFoundError(f'XSD file \'{xsd_path}\' does not exist')
            xml_schema: XMLSchema = XMLSchema(xsd_path)
            xml_element_tree: ElementTree = ElementTree(
                self._generate_xml_element(xml_schema.elements[root_element_name])
            )
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
        except Exception as ex:
            self._log.error(f'Exception found while generating  XML: {ex.__class__.__name__} - {ex}')
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
        xml_element: Element
        if xsd_element.type.model_group is not None:
            xml_element = self._generate_xml_group_element(xsd_element)
        else:
            xml_element = Element(xsd_element.local_name)
            xml_element.text = self._xml_simple_type_value_generator.generate_xml_simple_type_value(
                xsd_element.type.content
            )

        attribute_name: str
        xsd_attribute: XsdAttribute
        for attribute_name, xsd_attribute in xsd_element.attributes.items():
            if xsd_attribute.fixed is not None:
                xml_element.attrib[attribute_name] = xsd_element.fixed
            elif xsd_attribute.default is not None and self._force_default_value:
                xml_element.attrib[attribute_name] = xsd_element.default
            else:
                xml_element.attrib[attribute_name] = (
                    self._xml_simple_type_value_generator.generate_xml_simple_type_value(xsd_attribute.type)
                )
        return xml_element

    def _generate_xml_group_element(self, xsd_element: XsdElement) -> Element:
        xml_element: Element = Element(xsd_element.local_name)
        xsd_group: XsdGroup = xsd_element.type.content
        if xsd_group.model == 'all':
            x: XsdElement | XsdGroup
            for x in xsd_group.content:
                if random.choice([True, False]):
                    if isinstance(x, XsdElement):
                        xml_element.append(self._generate_xml_element(x))
                    elif isinstance(x, XsdGroup):
                        xml_element.append(self._generate_xml_group_element(x))
                    else:
                        raise NotImplementedError(f'Unknown group content {x}')
        elif xsd_group.model == 'choice':
            x: XsdElement | XsdGroup = random.choice(xsd_group.content)
            if isinstance(x, XsdElement):
                xml_element.append(self._generate_xml_element(x))
            elif isinstance(x, XsdGroup):
                xml_element.append(self._generate_xml_group_element(x))
            else:
                raise NotImplementedError(f'Unknown group content {x}')
        elif xsd_group.model == 'sequence':
            x: XsdElement | XsdGroup
            for x in xsd_group.content:
                if isinstance(x, XsdElement):
                    xml_element.append(self._generate_xml_element(x))
                elif isinstance(x, XsdGroup):
                    xml_element.append(self._generate_xml_group_element(x))
                else:
                    raise NotImplementedError(f'Unknown group content {x}')
        else:
            raise NotImplementedError(f'Unknown group model \'{xsd_group.model}\'')
        return xml_element
