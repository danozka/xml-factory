from dataclasses import dataclass, field

from xml_factory.domain.component import Component
from xml_factory.domain.element import Element
from xml_factory.domain.group_type import GroupType


@dataclass
class Group(Component):
    content: list[Element | 'Group'] = field(default_factory=list)
    min_occurs: int = 1
    max_occurs: int | None = 1
    type: GroupType | None = None
