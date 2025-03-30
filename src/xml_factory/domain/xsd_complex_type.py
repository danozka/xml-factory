from dataclasses import dataclass, field
from typing import Optional, Union

from xml_factory.domain.xsd_attribute import XsdAttribute
from xml_factory.domain.xsd_component import XsdComponent
from xml_factory.domain.xsd_group import XsdGroup


@dataclass
class XsdComplexType(XsdComponent):
    """Element that can contain attributes and child elements"""
    mixed: bool = False
    content_model: Optional[XsdGroup] = None
    attributes: dict[str, XsdAttribute] = field(default_factory=dict)
    base_type: Optional[Union[str, 'XsdComplexType']] = None
    derived_by: Optional[str] = None  # 'extension' or 'restriction'
