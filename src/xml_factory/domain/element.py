from dataclasses import dataclass
from typing import Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from xml_factory.domain.complex_type import ComplexType
from xml_factory.domain.component import Component
from xml_factory.domain.simple_type import SimpleType


@dataclass
class Element(Component):
    type: Optional[Union[str, SimpleType, 'ComplexType']] = None
    min_occurs: int = 1
    max_occurs: int | None = 1
    nillable: bool = False
    default: str | None = None
    fixed: str | None = None
    substitution_group: str | None = None
