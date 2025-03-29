from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, TYPE_CHECKING, Union

from xml_factory.domain.xsd_component import XsdComponent
if TYPE_CHECKING:
    from xml_factory.domain.xsd_simple_type import XsdSimpleType


@dataclass
class XsdRestriction(XsdComponent):
    """Constraint for simple types"""
    base: Optional[Union[str, 'XsdSimpleType']] = None
    facets: Dict[str, Any] = field(default_factory=dict)  # e.g., {'minLength': 1, 'pattern': '[A-Z]'}
    enumeration: Optional[List[str]] = None
