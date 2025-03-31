from dataclasses import dataclass, field
from typing import Optional, Union

from xml_factory.domain.xsd_base_type import XsdBaseType
from xml_factory.domain.xsd_simple_type import XsdSimpleType
from xml_factory.domain.xsd_white_space_restriction import XsdWhiteSpaceRestriction


@dataclass
class XsdRestriction(XsdSimpleType):
    """Constraint for simple types"""
    base: Optional[Union[XsdBaseType, XsdSimpleType]] = field(default=None)
    enumeration: Optional[list[str]] = field(default=None, repr=False)
    pattern: Optional[str] = field(default=None, repr=False)
    min_length: Optional[int] = field(default=None, repr=False)
    max_length: Optional[int] = field(default=None, repr=False)
    min_inclusive: Optional[Union[float, int]] = field(default=None, repr=False)
    max_inclusive: Optional[Union[float, int]] = field(default=None, repr=False)
    min_exclusive: Optional[Union[float, int]] = field(default=None, repr=False)
    max_exclusive: Optional[Union[float, int]] = field(default=None, repr=False)
    total_digits: Optional[int] = field(default=None, repr=False)
    fraction_digits: Optional[int] = field(default=None, repr=False)
    white_space: Optional[XsdWhiteSpaceRestriction] = field(default=None, repr=False)
