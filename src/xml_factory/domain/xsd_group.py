from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING

from xml_factory.domain.xsd_component import XsdComponent
from xml_factory.domain.xsd_element import XsdElement
from xml_factory.domain.xsd_group_type import XsdGroupType


@dataclass
class XsdGroup(XsdComponent):
    """Reusable group of elements"""
    elements: list[XsdElement] = field(default_factory=list)
    min_occurs: int = 1
    max_occurs: Optional[int] = 1
    type: Optional[XsdGroupType] = None

