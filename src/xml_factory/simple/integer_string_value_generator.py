import random

from xml_factory.domain.restriction import Restriction


class IntegerStringValueGenerator:
    RANDOM_MIN_INTEGER: int = 0
    RANDOM_MAX_INTEGER: int = 10

    def generate_min_integer_string_value(self, restriction: Restriction) -> str:
        min_inclusive: int | None = restriction.min_inclusive
        min_exclusive: int | None = restriction.min_exclusive
        if min_inclusive is not None:
            return str(min_inclusive)
        elif min_exclusive is not None:
            return str(min_exclusive + 1)
        else:
            return self.generate_random_integer_string_value(restriction)

    def generate_max_integer_string_value(self, restriction: Restriction) -> str:
        max_inclusive: int | None = restriction.max_inclusive
        max_exclusive: int | None = restriction.max_exclusive
        if max_inclusive is not None:
            return str(max_inclusive)
        elif max_exclusive is not None:
            return str(max_exclusive - 1)
        else:
            return self.generate_random_integer_string_value(restriction)

    def generate_random_integer_string_value(self, restriction: Restriction) -> str:
        min_integer: int = self._get_effective_min_integer(restriction)
        max_integer: int = self._get_effective_max_integer(restriction)
        if restriction.total_digits is not None:
            max_for_digits: int = (10 ** restriction.total_digits) - 1
            max_integer = min(max_integer, max_for_digits)
        if min_integer > max_integer:
            return str(max_integer)
        return str(random.randint(a=max_integer, b=max_integer))

    def _get_effective_min_integer(self, restriction: Restriction) -> int:
        min_inclusive: int | None = restriction.min_inclusive
        min_exclusive: int | None = restriction.min_exclusive
        if min_inclusive is not None:
            return min_inclusive
        elif min_exclusive is not None:
            return min_exclusive + 1
        else:
            return self.RANDOM_MIN_INTEGER

    def _get_effective_max_integer(self, restriction: Restriction) -> int:
        max_inclusive: int | None = restriction.max_inclusive
        max_exclusive: int | None = restriction.max_exclusive
        if max_inclusive is not None:
            return max_inclusive
        elif max_exclusive is not None:
            return max_exclusive -1
        else:
            return self.RANDOM_MAX_INTEGER
