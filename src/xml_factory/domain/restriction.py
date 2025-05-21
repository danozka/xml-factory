from dataclasses import dataclass

from xmlschema.aliases import AtomicValueType

from xml_factory.domain.base_type import BaseType


@dataclass
class Restriction:
    base_type: BaseType | None = None
    enumeration: list[str] | None = None
    pattern: str | None = None
    length: int | None = None
    min_length: int | None = None
    max_length: int | None = None
    min_inclusive: AtomicValueType | None = None
    max_inclusive: AtomicValueType | None = None
    min_exclusive: AtomicValueType | None = None
    max_exclusive: AtomicValueType | None = None
    total_digits: int | None = None
    fraction_digits: int | None = None
