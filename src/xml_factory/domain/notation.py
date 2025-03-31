from dataclasses import dataclass
from typing import Optional

from xml_factory.domain.xsd_component import XsdComponent


@dataclass
class XsdNotation(XsdComponent):
    """XML notation declaration"""
    system: Optional[str] = None
    public: Optional[str] = None
