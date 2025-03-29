from dataclasses import dataclass, field
from typing import List, TYPE_CHECKING

from xml_factory.domain.xsd_component import XsdComponent
if TYPE_CHECKING:
    from xml_factory.domain.xsd_element import XsdElement


@dataclass
class XsdContentModel(XsdComponent):
    """Base for content model groups"""
    elements: List['XsdElement'] = field(default_factory=list)
