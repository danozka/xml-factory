from dataclasses import dataclass

from xml_factory.domain.attribute_use import AttributeUse
from xml_factory.domain.component import Component
from xml_factory.domain.simple_type import SimpleType


@dataclass
class Attribute(Component):
    type: str | SimpleType | None = None
    use: AttributeUse = AttributeUse.optional
    default: str | None = None
    fixed: str | None = None
