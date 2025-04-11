import logging
from logging import Logger

from xmlschema.validators import (
    XMLSchemaBase,
    XsdAtomic,
    XsdAtomicBuiltin,
    XsdAttribute,
    XsdAttributeGroup,
    XsdComplexType,
    XsdElement,
    XsdFacet,
    XsdFractionDigitsFacet,
    XsdGroup,
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
    XsdUnion,
    XsdWhiteSpaceFacet
)

from xml_factory.domain.attribute import Attribute
from xml_factory.domain.attribute_use import AttributeUse
from xml_factory.domain.base_type import BaseType
from xml_factory.domain.complex_type import ComplexType
from xml_factory.domain.element import Element
from xml_factory.domain.form_default import FormDefault
from xml_factory.domain.group import Group
from xml_factory.domain.group_type import GroupType
from xml_factory.domain.list import List
from xml_factory.domain.restriction import Restriction
from xml_factory.domain.schema import Schema
from xml_factory.domain.simple_type import SimpleType
from xml_factory.domain.union import Union
from xml_factory.domain.white_space_restriction import WhiteSpaceRestriction


class XmlschemaAdapter:
    _log: Logger = logging.getLogger(__name__)

    def adapt_xmlschema_schema(self, xmlschema_schema: XMLSchemaBase) -> Schema:
        self._log.debug(f'Adapting {xmlschema_schema}...')
        result: Schema = Schema(
            target_namespace=xmlschema_schema.target_namespace,
            element_form_default=FormDefault(xmlschema_schema.element_form_default),
            attribute_form_default=FormDefault(xmlschema_schema.attribute_form_default),
            elements={
                element_name: self.adapt_xmlschema_element(element)
                for element_name, element in xmlschema_schema.elements.items()
            },
            imports={
                import_name: self.adapt_xmlschema_schema(import_)
                for import_name, import_ in xmlschema_schema.imports.items()
            },
            includes=[self.adapt_xmlschema_schema(include) for include in xmlschema_schema.includes.values()]
        )
        self._log.debug(f'{xmlschema_schema} adapted')
        return result

    def adapt_xmlschema_simple_type(self, xmlschema_simple_type: XsdSimpleType) -> SimpleType:
        if isinstance(xmlschema_simple_type, XsdAtomic):
            self._log.debug(f'Adapting restriction {xmlschema_simple_type}...')
            result: Restriction = Restriction(
                name=xmlschema_simple_type.local_name,
                base_type=BaseType(
                    xmlschema_simple_type.local_name
                    if isinstance(xmlschema_simple_type, XsdAtomicBuiltin)
                    else xmlschema_simple_type.base_type.local_name
                ),
                enumeration=xmlschema_simple_type.enumeration
            )
            xmlschema_facet: XsdFacet
            for facet in xmlschema_simple_type.facets.values():
                if isinstance(facet, XsdFractionDigitsFacet):
                    result.fraction_digits = facet.value
                elif isinstance(facet, XsdMaxExclusiveFacet):
                    result.max_exclusive = float(facet.value)
                elif isinstance(facet, XsdMaxInclusiveFacet):
                    result.max_inclusive = float(facet.value)
                elif isinstance(facet, XsdMaxLengthFacet):
                    result.max_length = facet.value
                elif isinstance(facet, XsdMinExclusiveFacet):
                    result.min_exclusive = float(facet.value)
                elif isinstance(facet, XsdMinInclusiveFacet):
                    result.min_inclusive = float(facet.value)
                elif isinstance(facet, XsdMinLengthFacet):
                    result.min_length = int(facet.value)
                elif isinstance(facet, XsdPatternFacets):
                    result.pattern = facet.regexps[0]
                elif isinstance(facet, XsdTotalDigitsFacet):
                    result.total_digits = facet.value
                elif isinstance(facet, XsdWhiteSpaceFacet):
                    result.white_space = WhiteSpaceRestriction(facet.value)
            self._log.debug(f'Restriction {xmlschema_simple_type} adapted')
        elif isinstance(xmlschema_simple_type, XsdUnion):
            self._log.debug(f'Adapting union {xmlschema_simple_type}...')
            result: Union = Union(
                name=xmlschema_simple_type.local_name,
                member_types=[self.adapt_xmlschema_simple_type(x) for x in xmlschema_simple_type.member_types]
            )
            self._log.debug(f'Union {xmlschema_simple_type} adapted')
        elif isinstance(xmlschema_simple_type, XsdList):
            self._log.debug(f'Adapting list {xmlschema_simple_type}...')
            result: List = List(
                name=xmlschema_simple_type.local_name,
                item_type=self.adapt_xmlschema_simple_type(xmlschema_simple_type.item_type)
            )
            self._log.debug(f'List {xmlschema_simple_type} adapted')
        else:
            raise NotImplementedError(f'Unknown simple type {xmlschema_simple_type}')
        return result

    def adapt_xmlschema_complex_type(self, xmlschema_complex_type: XsdComplexType) -> ComplexType:
        self._log.debug(f'Adapting complex type {xmlschema_complex_type}...')
        if isinstance(xmlschema_complex_type.content, XsdSimpleType):
            content: SimpleType = self.adapt_xmlschema_simple_type(xmlschema_complex_type.content)
        elif isinstance(xmlschema_complex_type.content, XsdGroup):
            content: Group = self.adapt_xmlschema_group(xmlschema_complex_type.content)
        else:
            raise NotImplementedError(f'Unknown complex type content {xmlschema_complex_type.content}')
        result: ComplexType = ComplexType(
            name=xmlschema_complex_type.local_name,
            mixed=xmlschema_complex_type.mixed,
            content=content,
            attributes=[self.adapt_xmlschema_attribute(x) for x in xmlschema_complex_type.attributes.values()]
        )
        self._log.debug(f'Complex type {xmlschema_complex_type} adapted')
        return result

    def adapt_xmlschema_group(self, xmlschema_group: XsdGroup) -> Group:
        self._log.debug(f'Adapting group {xmlschema_group}...')
        content: list[Element | Group] = []
        x: XsdElement | XsdGroup
        for x in xmlschema_group.content:
            if isinstance(x, XsdElement):
                content.append(self.adapt_xmlschema_element(x))
            elif isinstance(x, XsdGroup):
                content.append(self.adapt_xmlschema_group(x))
            else:
                raise NotImplementedError(f'Unknown group content {x}')
        result: Group = Group(
            name=xmlschema_group.local_name,
            content=content,
            min_occurs=xmlschema_group.min_occurs,
            max_occurs=xmlschema_group.max_occurs,
            type=GroupType(xmlschema_group.model)
        )
        self._log.debug(f'Group {xmlschema_group} adapted')
        return result

    def adapt_xmlschema_attribute(self, xmlschema_attribute: XsdAttribute) -> Attribute:
        self._log.debug(f'Adapting attribute {xmlschema_attribute}...')
        result: Attribute = Attribute(
            name=xmlschema_attribute.local_name,
            type=self.adapt_xmlschema_simple_type(xmlschema_attribute.type),
            use=AttributeUse(xmlschema_attribute.use),
            default=xmlschema_attribute.default,
            fixed=xmlschema_attribute.fixed
        )
        self._log.debug(f'Attribute {xmlschema_attribute} adapted')
        return result

    def adapt_xmlschema_element(self, xmlschema_element: XsdElement) -> Element:
        self._log.debug(f'Adapting element {xmlschema_element}...')
        result: Element = Element(
            name=xmlschema_element.local_name,
            type=(
                self.adapt_xmlschema_simple_type(xmlschema_element.type)
                if isinstance(xmlschema_element.type, XsdSimpleType)
                else self.adapt_xmlschema_complex_type(xmlschema_element.type)
            ),
            min_occurs=xmlschema_element.min_occurs,
            max_occurs=xmlschema_element.max_occurs,
            default=xmlschema_element.default,
            fixed=xmlschema_element.fixed
        )
        self._log.debug(f'Element {xmlschema_element} adapted')
        return result
