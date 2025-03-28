from dataclasses import dataclass
from typing import Any, List, Dict, Union, Optional

from xml_factory.domain.xsd_component import XsdComponent
from xml_factory.domain.xsd_simple_type import XsdSimpleType


@dataclass
class XsdRestriction(XsdComponent):
    """Constraint for simple types"""
    base: Union[str, XsdSimpleType]
    facets: Dict[str, Any]  # e.g., {'minLength': 1, 'pattern': '[A-Z]'}
    enumeration: Optional[List[str]] = None
