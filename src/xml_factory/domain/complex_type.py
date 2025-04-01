from dataclasses import dataclass, field

from xml_factory.domain.attribute import Attribute
from xml_factory.domain.complex_derivation_type import ComplexDerivationType
from xml_factory.domain.component import Component
from xml_factory.domain.group import Group
from xml_factory.domain.simple_type import SimpleType


@dataclass
class ComplexType(Component):
    mixed: bool = False
    content: SimpleType | Group | None = None
    attributes: dict[str, Attribute] = field(default_factory=dict)
    derived_by: ComplexDerivationType | None = None
