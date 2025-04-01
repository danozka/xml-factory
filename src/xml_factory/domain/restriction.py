from dataclasses import dataclass, field

from xml_factory.domain.base_type import BaseType
from xml_factory.domain.simple_type import SimpleType
from xml_factory.domain.white_space_restriction import WhiteSpaceRestriction


@dataclass
class Restriction(SimpleType):
    base: BaseType | SimpleType | None = field(default=None)
    enumeration: list[str] | None = field(default=None, repr=False)
    pattern: str | None = field(default=None, repr=False)
    min_length: int | None = field(default=None, repr=False)
    max_length: int | None = field(default=None, repr=False)
    min_inclusive: float | int | None = field(default=None, repr=False)
    max_inclusive: float | int | None = field(default=None, repr=False)
    min_exclusive: float | int | None = field(default=None, repr=False)
    max_exclusive: float | int | None = field(default=None, repr=False)
    total_digits: int | None = field(default=None, repr=False)
    fraction_digits: int | None = field(default=None, repr=False)
    white_space: WhiteSpaceRestriction | None = field(default=None, repr=False)
