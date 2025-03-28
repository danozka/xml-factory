from dataclasses import dataclass
from typing import List

from xml_factory.domain.xsd_component import XsdComponent
from xml_factory.domain.xsd_element import XsdElement


@dataclass
class XsdContentModel(XsdComponent):
    """Base for content model groups"""
    elements: List[XsdElement]
