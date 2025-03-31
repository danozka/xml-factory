import logging
from logging import Logger
from typing import Type

from xmlschema.validators import (
    XMLSchemaBase as XmlschemaSchema,
    XsdAtomic as XmlschemaAtomic,
    XsdAtomicBuiltin as XmlschemaAtomicBuiltin,
    XsdComplexType as XmlschemaComplexType,
    XsdFacet as XmlschemaFacet,
    XsdFractionDigitsFacet as XmlschemaFractionDigitsFacet,
    XsdGroup as XmlschemaGroup,
    XsdList as XmlschemaList,
    XsdMaxExclusiveFacet as XmlschemaMaxExclusiveFacet,
    XsdMaxInclusiveFacet as XmlschemaMaxInclusiveFacet,
    XsdMaxLengthFacet as XmlschemaMaxLengthFacet,
    XsdMinExclusiveFacet as XmlschemaMinExclusiveFacet,
    XsdMinInclusiveFacet as XmlschemaMinInclusiveFacet,
    XsdMinLengthFacet as XmlschemaMinLengthFacet,
    XsdPatternFacets as XmlschemaPatternFacets,
    XsdSimpleType as XmlschemaSimpleType,
    XsdTotalDigitsFacet as XmlschemaTotalDigitsFacet,
    XsdUnion as XmlschemaUnion,
    XsdWhiteSpaceFacet as XmlschemaWhiteSpaceFacet
)

from xml_factory.domain.xsd_all import XsdAll
from xml_factory.domain.xsd_attribute import XsdAttribute
from xml_factory.domain.xsd_attribute_use import XsdAttributeUse
from xml_factory.domain.xsd_attribute_group import XsdAttributeGroup
from xml_factory.domain.xsd_base_type import XsdBaseType
from xml_factory.domain.xsd_choice import XsdChoice
from xml_factory.domain.xsd_complex_type import XsdComplexType
from xml_factory.domain.xsd_complex_type_derivation_type import XsdComplexTypeDerivationType
from xml_factory.domain.xsd_form_default import XsdFormDefault
from xml_factory.domain.xsd_group import XsdGroup
from xml_factory.domain.xsd_list import XsdList
from xml_factory.domain.xsd_notation import XsdNotation
from xml_factory.domain.xsd_restriction import XsdRestriction
from xml_factory.domain.xsd_schema import XsdSchema
from xml_factory.domain.xsd_sequence import XsdSequence
from xml_factory.domain.xsd_simple_type import XsdSimpleType
from xml_factory.domain.xsd_union import XsdUnion
from xml_factory.domain.xsd_white_space_restriction import XsdWhiteSpaceRestriction


class XmlschemaAdapter:
    _log: Logger = logging.getLogger(__name__)

    def adapt_xmlschema_schema(self, xmlschema_schema: XmlschemaSchema) -> XsdSchema:
        self._log.debug(f'Adapting {xmlschema_schema}...')
        simple_types: dict[str, XsdSimpleType] = {
            xmlschema_simple_type.name: self.adapt_xmlschema_simple_type(xmlschema_simple_type)
            for xmlschema_simple_type in xmlschema_schema.simple_types
        }
        complex_types: dict[str, XsdComplexType] = {
            xmlschema_complex_type.name: self.adapt_xmlschema_complex_type(xmlschema_complex_type)
            for xmlschema_complex_type in xmlschema_schema.complex_types
        }
        result: XsdSchema = XsdSchema(
            target_namespace=xmlschema_schema.target_namespace,
            element_form_default=XsdFormDefault(xmlschema_schema.element_form_default),
            attribute_form_default=XsdFormDefault(xmlschema_schema.attribute_form_default),
            elements=self._adapt_xmlschema_elements(xmlschema_schema),
            simple_types=simple_types,
            complex_types=complex_types,
            attribute_groups={
                attr_group_name: XsdAttributeGroup(
                    name=attr_group.name,
                    attributes={
                        attr_name: XsdAttribute(
                            name=attr.name,
                            type=attr.type,
                            use=XsdAttributeUse(attr.use),
                            default=attr.default,
                            fixed=attr.fixed
                        )
                        for attr_name, attr in attr_group.items()
                    }
                )
                for attr_group_name, attr_group in xmlschema_schema.attribute_groups.items()
            },
            groups={
                group_name: XsdGroup(
                    name=group.name,
                    elements=[...],
                    min_occurs=group.min_occurs,
                    max_occurs=group.max_occurs,
                    type=XsdGroupType(group.model)
                )
                for group_name, group in xmlschema_schema.groups.items()
            },
            notations={
                notation_name: XsdNotation(
                    name=notation.name,
                    system=notation.system,
                    public=notation.public
                )
                for notation_name, notation in xmlschema_schema.notations.items()
            },
            imports={
                import_name: self.adapt_xmlschema_schema(import_)
                for import_name, import_ in xmlschema_schema.imports.items()
            },
            includes=[self.adapt_xmlschema_schema(include) for include in xmlschema_schema.includes.values()]
        )
        self._log.debug(f'{xmlschema_schema} adapted')
        return result

    def adapt_xmlschema_simple_type(self, xmlschema_simple_type: XmlschemaSimpleType) -> XsdSimpleType:
        if isinstance(xmlschema_simple_type, XmlschemaAtomic):
            self._log.debug(f'Adapting restriction {xmlschema_simple_type}...')
            result: XsdRestriction = XsdRestriction(
                name=xmlschema_simple_type.local_name,
                base=XsdBaseType(
                    xmlschema_simple_type.local_name
                    if isinstance(xmlschema_simple_type, XmlschemaAtomicBuiltin)
                    else xmlschema_simple_type.base_type.local_name
                ),
                enumeration=xmlschema_simple_type.enumeration
            )
            xmlschema_facet: XmlschemaFacet
            for facet in xmlschema_simple_type.facets.values():
                if isinstance(facet, XmlschemaFractionDigitsFacet):
                    result.fraction_digits = facet.value
                elif isinstance(facet, XmlschemaMaxExclusiveFacet):
                    result.max_exclusive = float(facet.value)
                elif isinstance(facet, XmlschemaMaxInclusiveFacet):
                    result.max_inclusive = float(facet.value)
                elif isinstance(facet, XmlschemaMaxLengthFacet):
                    result.max_length = facet.value
                elif isinstance(facet, XmlschemaMinExclusiveFacet):
                    result.min_exclusive = float(facet.value)
                elif isinstance(facet, XmlschemaMinInclusiveFacet):
                    result.min_inclusive = float(facet.value)
                elif isinstance(facet, XmlschemaMinLengthFacet):
                    result.min_length = int(facet.value)
                elif isinstance(facet, XmlschemaPatternFacets):
                    result.pattern = facet.regexps[0]
                elif isinstance(facet, XmlschemaTotalDigitsFacet):
                    result.total_digits = facet.value
                elif isinstance(facet, XmlschemaWhiteSpaceFacet):
                    result.white_space = XsdWhiteSpaceRestriction(facet.value)
            self._log.debug(f'Restriction {xmlschema_simple_type} adapted')
        elif isinstance(xmlschema_simple_type, XmlschemaUnion):
            self._log.debug(f'Adapting union {xmlschema_simple_type}...')
            result: XsdUnion = XsdUnion(
                name=xmlschema_simple_type.local_name,
                member_types=[self.adapt_xmlschema_simple_type(x) for x in xmlschema_simple_type.member_types]
            )
            self._log.debug(f'Union {xmlschema_simple_type} adapted')
        elif isinstance(xmlschema_simple_type, XmlschemaList):
            self._log.debug(f'Adapting list {xmlschema_simple_type}...')
            result: XsdList = XsdList(
                name=xmlschema_simple_type.local_name,
                item_type=self.adapt_xmlschema_simple_type(xmlschema_simple_type.item_type)
            )
            self._log.debug(f'List {xmlschema_simple_type} adapted')
        else:
            raise ValueError(f'Unknown simple type {xmlschema_simple_type}')
        return result

    def adapt_xmlschema_complex_type(self, xmlschema_complex_type: XmlschemaComplexType) -> XsdComplexType:
        self._log.debug(f'Adapting complex type {xmlschema_complex_type}...')
        content: XsdSimpleType | XsdGroup | None = None
        if isinstance(xmlschema_complex_type.content, XmlschemaSimpleType):
            content: XsdSimpleType = self.adapt_xmlschema_simple_type(xmlschema_complex_type.content)
        elif isinstance(xmlschema_complex_type.content, XmlschemaGroup):
            if xmlschema_complex_type.content.model == 'sequence':
                content_class = XsdAll
            content: XsdAll = XsdAll(
                name=xmlschema_complex_type.content.local_name,
                elements=[

                ],
                min_occurs=xmlschema_complex_type.content.min_occurs,
                max_occurs=xmlschema_complex_type.content.max_occurs
            )
        else:
            raise ValueError(f'Unknown complex type content {xmlschema_complex_type.content}')
        result: XsdComplexType = XsdComplexType(
            name=xmlschema_complex_type.local_name,
            mixed=xmlschema_complex_type.mixed,
            content=content,
            attributes={},
            derived_by=(
                XsdComplexTypeDerivationType(xmlschema_complex_type.derivation)
                if xmlschema_complex_type.derivation is not None
                else None
            )
        )
        self._log.debug(f'Complex type {xmlschema_complex_type} adapted')
        return result
