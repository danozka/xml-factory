from dataclasses import dataclass
from typing import List, Optional

from xml_factory.domain.xsd_component import XsdComponent
from xml_factory.domain.xsd_restriction import XsdRestriction


@dataclass
class XsdSimpleType(XsdComponent):
    """Base for simple types (value-only elements)"""
    restriction: Optional[XsdRestriction] = None
    union: Optional[List['XsdSimpleType']] = None
    list: Optional['XsdSimpleType'] = None
