from dataclasses import dataclass, field
from typing import Optional, Union

from xml_factory.domain.xsd_attribute import XsdAttribute
from xml_factory.domain.xsd_complex_type_derivation_type import XsdComplexTypeDerivationType
from xml_factory.domain.xsd_component import XsdComponent
from xml_factory.domain.xsd_group import XsdGroup
from xml_factory.domain.xsd_simple_type import XsdSimpleType


@dataclass
class XsdComplexType(XsdComponent):
    """Element that can contain attributes and child elements"""
    mixed: bool = False
    content: Optional[Union[XsdSimpleType, XsdGroup]] = None
    attributes: dict[str, XsdAttribute] = field(default_factory=dict)
    derived_by: Optional[XsdComplexTypeDerivationType] = None
