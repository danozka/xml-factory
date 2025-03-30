from dataclasses import dataclass
from typing import Optional, Union

from xml_factory.domain.xsd_attribute_use import XsdAttributeUse
from xml_factory.domain.xsd_component import XsdComponent
from xml_factory.domain.xsd_simple_type import XsdSimpleType


@dataclass
class XsdAttribute(XsdComponent):
    """Attribute declaration"""
    type: Optional[Union[str | XsdSimpleType]]= None
    use: XsdAttributeUse = XsdAttributeUse.optional
    default: Optional[str] = None
    fixed: Optional[str] = None
