import math
import random

from xml_factory.domain.restriction import Restriction


class DecimalStringValueGenerator:
    @staticmethod
    def generate_decimal_string_value(value: float, fraction_digits: int | None = None) -> str:
        if fraction_digits is None:
            fraction_digits = 2
        return f'{value:.{fraction_digits}f}'

    @staticmethod
    def generate_random_decimal_string_value(restriction: Restriction) -> str:
        min_inclusive: float | None = restriction.min_inclusive
        max_inclusive: float | None = restriction.max_inclusive
        min_exclusive: float | None = restriction.min_exclusive
        max_exclusive: float | None = restriction.max_exclusive
        fraction_digits: int | None = restriction.fraction_digits
        if restriction.pattern is not None:
            return input(f'[{restriction.name}] Input decimal for the regular expression \'{restriction.pattern}\': ')
        if min_inclusive is None:
            min_inclusive = 0.0
        if max_inclusive is None:
            max_inclusive = 1.0
        if min_exclusive is not None and min_exclusive > min_inclusive:
            min_inclusive = min_exclusive + 1e-6
        if max_exclusive is not None and max_exclusive < max_inclusive:
            max_inclusive = max_exclusive - 1e-6
        if fraction_digits is None:
            fraction_digits = 2

        integer_part: int = int(random.uniform(a=min_inclusive, b=max_inclusive))
        fractional_number: float
        fractional_number, _ = math.modf(max_inclusive)
        fractional_number *= 10 ** fraction_digits
        max_fractional_part: int = min(int(fractional_number), (10 ** fraction_digits) - 1)
        fractional_part: int = random.randint(a=0, b=max_fractional_part)
        return f'{integer_part}.{fractional_part:0{fraction_digits}}'
