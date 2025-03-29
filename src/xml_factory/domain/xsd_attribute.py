from dataclasses import dataclass
from typing import Optional, Union

from xml_factory.domain.xsd_component import XsdComponent
from xml_factory.domain.xsd_simple_type import XsdSimpleType


@dataclass
class XsdAttribute(XsdComponent):
    """Attribute declaration"""
    type: Optional[Union[str, XsdSimpleType]] = None
    use: str = 'optional'  # 'required' | 'prohibited' | 'optional'
    default: Optional[str] = None
    fixed: Optional[str] = None
