import random

from xml_factory.domain.restriction import Restriction


class IntegerStringValueGenerator:
    @staticmethod
    def generate_random_integer_string_value(restriction: Restriction) -> str:
        min_inclusive: int | None = (
            int(restriction.min_inclusive) if restriction.min_inclusive is not None else restriction.min_inclusive
        )
        max_inclusive: int | None = (
            int(restriction.max_inclusive) if restriction.max_inclusive is not None else restriction.max_inclusive
        )
        min_exclusive: int | None = (
            int(restriction.min_exclusive) if restriction.min_exclusive is not None else restriction.min_exclusive
        )
        max_exclusive: int | None = (
            int(restriction.max_exclusive) if restriction.max_exclusive is not None else restriction.max_exclusive
        )
        total_digits: int = restriction.total_digits
        if min_inclusive is None:
            min_inclusive = 0
        if max_inclusive is None:
            max_inclusive = 10
        if min_exclusive is not None and min_exclusive > min_inclusive:
            min_inclusive = min_exclusive + 1
        if max_exclusive is not None and max_exclusive < max_inclusive:
            max_inclusive = max_exclusive - 1
        if total_digits is not None:
            min_inclusive = max(min_inclusive, 10 ** (total_digits - 1))
            max_inclusive = min(max_inclusive, (10 ** total_digits) - 1)
        return str(random.randint(a=min_inclusive, b=max_inclusive))
