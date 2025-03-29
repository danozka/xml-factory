from dataclasses import dataclass
from typing import Optional, Union

from xml_factory.domain.xsd_complex_type import XsdComplexType
from xml_factory.domain.xsd_component import XsdComponent
from xml_factory.domain.xsd_simple_type import XsdSimpleType


@dataclass
class XsdElement(XsdComponent):
    """Element declaration"""
    type: Optional[Union[str, XsdSimpleType, XsdComplexType]] = None
    min_occurs: int = 1
    max_occurs: Union[int, str] = 1
    nillable: bool = False
    default: Optional[str] = None
    fixed: Optional[str] = None
    substitution_group: Optional[str] = None
