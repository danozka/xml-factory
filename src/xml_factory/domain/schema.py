from dataclasses import dataclass, field
from typing import Optional

from xml_factory.domain.xsd_attribute_group import XsdAttributeGroup
from xml_factory.domain.xsd_complex_type import XsdComplexType
from xml_factory.domain.xsd_element import XsdElement
from xml_factory.domain.xsd_form_default import XsdFormDefault
from xml_factory.domain.xsd_group import XsdGroup
from xml_factory.domain.xsd_notation import XsdNotation
from xml_factory.domain.xsd_simple_type import XsdSimpleType


@dataclass
class XsdSchema:
    """Root schema container"""
    target_namespace: Optional[str] = None
    element_form_default: XsdFormDefault = XsdFormDefault.unqualified
    attribute_form_default: XsdFormDefault = XsdFormDefault.unqualified
    elements: dict[str, XsdElement] = field(default_factory=dict)
    simple_types: dict[str, XsdSimpleType] = field(default_factory=dict)
    complex_types: dict[str, XsdComplexType] = field(default_factory=dict)
    attribute_groups: dict[str, XsdAttributeGroup] = field(default_factory=dict)
    groups: dict[str, XsdGroup] = field(default_factory=dict)
    notations: dict[str, XsdNotation] = field(default_factory=dict)
    imports: dict[str, Optional['XsdSchema']] = field(default_factory=dict)
    includes: list['XsdSchema'] = field(default_factory=list)
