from dataclasses import dataclass, field

from xml_factory.domain.xsd_attribute import XsdAttribute
from xml_factory.domain.xsd_component import XsdComponent


@dataclass
class XsdAttributeGroup(XsdComponent):
    """Reusable group of attributes"""
    attributes: dict[str, XsdAttribute] = field(default_factory=dict)
