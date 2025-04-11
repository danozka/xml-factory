from dataclasses import dataclass, field

from xml_factory.domain.base_type import BaseType
from xml_factory.domain.white_space_restriction import WhiteSpaceRestriction


@dataclass
class Restriction:
    name: str
    base_type: BaseType
    enumeration: list[str] | None = field(default=None, repr=False)
    pattern: str | None = field(default=None, repr=False)
    min_length: int | None = field(default=None, repr=False)
    max_length: int | None = field(default=None, repr=False)
    min_inclusive: float | None = field(default=None, repr=False)
    max_inclusive: float | None = field(default=None, repr=False)
    min_exclusive: float | None = field(default=None, repr=False)
    max_exclusive: float | None = field(default=None, repr=False)
    total_digits: int | None = field(default=None, repr=False)
    fraction_digits: int | None = field(default=None, repr=False)
    white_space: WhiteSpaceRestriction | None = field(default=None, repr=False)
