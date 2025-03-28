from dataclasses import dataclass
from typing import Dict, List, Optional

from xml_factory.domain.xsd_attribute_group import XsdAttributeGroup
from xml_factory.domain.xsd_complex_type import XsdComplexType
from xml_factory.domain.xsd_element import XsdElement
from xml_factory.domain.xsd_group import XsdGroup
from xml_factory.domain.xsd_notation import XsdNotation
from xml_factory.domain.xsd_simple_type import XsdSimpleType


@dataclass
class XsdSchema:
    """Root schema container"""
    target_namespace: Optional[str] = None
    element_form_default: str = 'unqualified'
    attribute_form_default: str = 'unqualified'
    elements: Dict[str, XsdElement] = None
    complex_types: Dict[str, XsdComplexType] = None
    simple_types: Dict[str, XsdSimpleType] = None
    attribute_groups: Dict[str, XsdAttributeGroup] = None
    groups: Dict[str, XsdGroup] = None
    notations: Dict[str, XsdNotation] = None
    imports: Dict[str, 'XsdSchema'] = None
    includes: List['XsdSchema'] = None
