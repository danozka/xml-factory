from dataclasses import dataclass, field

from xml_factory.domain.attribute import Attribute
from xml_factory.domain.component import Component


@dataclass
class AttributeGroup(Component):
    attributes: dict[str, Attribute] = field(default_factory=dict)
