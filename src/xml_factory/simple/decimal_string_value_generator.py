import random
from decimal import Decimal, localcontext, ROUND_DOWN, ROUND_HALF_EVEN, ROUND_UP

from xml_factory.domain.restriction import Restriction


class DecimalStringValueGenerator:
    RANDOM_MIN_DECIMAL: Decimal = Decimal('-1e10')
    RANDOM_MAX_DECIMAL: Decimal = Decimal('1e10')
    RANDOM_TOTAL_DIGITS: int = 10
    RANDOM_FRACTION_DIGITS: int = 2

    def generate_min_decimal_string_value(self, restriction: Restriction) -> str:
        total_digits: int
        fraction_digits: int
        total_digits, fraction_digits = self._get_total_and_fraction_digits(restriction)
        min_possible: Decimal = self._get_min_possible_value(total_digits=total_digits, fraction_digits=fraction_digits)
        min_value: Decimal
        if restriction.min_inclusive is not None:
            min_value = Decimal(str(restriction.min_inclusive))
        else:
            min_value = min_possible
        if restriction.min_exclusive is not None:
            min_step: Decimal = Decimal('0.' + '0' * (fraction_digits - 1) + '1' if fraction_digits > 0 else '1')
            min_exclusive_value = Decimal(str(restriction.min_exclusive)) + min_step
            min_value = max(min_value, min_exclusive_value)
        max_value: Decimal | None = None
        if restriction.max_inclusive is not None:
            max_value = Decimal(str(restriction.max_inclusive))
        if restriction.max_exclusive is not None:
            max_step: Decimal = Decimal('0.' + '0' * (fraction_digits - 1) + '1' if fraction_digits > 0 else '1')
            max_exclusive_value: Decimal = Decimal(str(restriction.max_exclusive)) - max_step
            if max_value is None or max_exclusive_value < max_value:
                max_value = max_exclusive_value
        if max_value is not None and min_value > max_value:
            return self._generate_decimal_string_value(value=max_value, fraction_digits=fraction_digits)
        with localcontext() as ctx:
            ctx.prec = total_digits + 2
            min_value = min_value.quantize(Decimal('0.' + '0' * fraction_digits), rounding=ROUND_UP)
            return self._generate_decimal_string_value(value=min_value, fraction_digits=fraction_digits)

    def generate_max_decimal_string_value(self, restriction: Restriction) -> str:
        total_digits: int
        fraction_digits: int
        total_digits, fraction_digits = self._get_total_and_fraction_digits(restriction)
        max_possible: Decimal = self._get_max_possible_value(total_digits=total_digits, fraction_digits=fraction_digits)
        max_value: Decimal = min(
            max_possible,
            Decimal(str(restriction.max_inclusive)) if restriction.max_inclusive is not None else max_possible
        )
        if restriction.max_exclusive is not None:
            max_step: Decimal = Decimal('0.' + '0' * (fraction_digits - 1) + '1' if fraction_digits > 0 else '1')
            max_value = min(max_value, Decimal(str(restriction.max_exclusive)) - max_step)
        min_value: Decimal | None = None
        if restriction.min_inclusive is not None:
            min_value = Decimal(str(restriction.min_inclusive))
        if restriction.min_exclusive is not None:
            min_step: Decimal = Decimal('0.' + '0' * (fraction_digits - 1) + '1' if fraction_digits > 0 else '1')
            min_exclusive_value = Decimal(str(restriction.min_exclusive)) + min_step
            if min_value is None or min_exclusive_value > min_value:
                min_value = min_exclusive_value
        if min_value is not None and min_value > max_value:
            return self._generate_decimal_string_value(value=min_value, fraction_digits=fraction_digits)
        with localcontext() as ctx:
            ctx.prec = total_digits + 2
            max_value = max_value.quantize(Decimal('0.' + '0' * fraction_digits), rounding=ROUND_DOWN)
            return self._generate_decimal_string_value(value=max_value, fraction_digits=fraction_digits)

    def generate_random_decimal_string_value(self, restriction: Restriction) -> str:
        total_digits: int
        fraction_digits: int
        total_digits, fraction_digits = self._get_total_and_fraction_digits(restriction)
        min_value: Decimal = (
            Decimal(str(restriction.min_inclusive))
            if restriction.min_inclusive is not None else self.RANDOM_MIN_DECIMAL
        )
        max_value: Decimal = (
            Decimal(str(restriction.max_inclusive))
            if restriction.max_inclusive is not None else self.RANDOM_MAX_DECIMAL
        )
        if restriction.min_exclusive is not None:
            min_step: Decimal = Decimal('0.' + '0' * (fraction_digits - 1) + '1' if fraction_digits > 0 else '1')
            min_value = max(min_value, Decimal(str(restriction.min_exclusive)) + min_step)
        if restriction.max_exclusive is not None:
            max_step: Decimal = Decimal('0.' + '0' * (fraction_digits - 1) + '1' if fraction_digits > 0 else '1')
            max_value = min(max_value, Decimal(str(restriction.max_exclusive)) - max_step)
        max_possible: Decimal = self._get_max_possible_value(total_digits=total_digits, fraction_digits=fraction_digits)
        max_value = min(max_value, max_possible)
        if min_value > max_value:
            return self._generate_decimal_string_value(min_value, fraction_digits)
        with localcontext() as ctx:
            ctx.prec = total_digits + 2
            scale: Decimal = Decimal(10) ** fraction_digits
            min_scaled: int = int((min_value * scale).to_integral_value(rounding=ROUND_HALF_EVEN))
            max_scaled: int = int((max_value * scale).to_integral_value(rounding=ROUND_HALF_EVEN))
            if min_scaled > max_scaled:
                min_scaled, max_scaled = max_scaled, min_scaled
            value_scaled: int = random.randint(a=min_scaled, b=max_scaled)
            value: Decimal = Decimal(value_scaled) / scale
            return self._generate_decimal_string_value(value=value, fraction_digits=fraction_digits)
    
    @staticmethod
    def _generate_decimal_string_value(value: Decimal, fraction_digits: int) -> str:
        return format(value, f'.{fraction_digits}f')

    def _get_total_and_fraction_digits(self, restriction: Restriction) -> tuple[int, int]:
        total_digits: int = (
            restriction.total_digits if restriction.total_digits is not None else self.RANDOM_TOTAL_DIGITS
        )
        fraction_digits: int = (
            restriction.fraction_digits if restriction.fraction_digits is not None else self.RANDOM_FRACTION_DIGITS
        )
        if total_digits <= fraction_digits:
            fraction_digits = total_digits - 1 if total_digits > 1 else 0
        return total_digits, fraction_digits

    @staticmethod
    def _get_max_possible_value(total_digits: int, fraction_digits: int) -> Decimal:
        int_digits: int = total_digits - fraction_digits
        return Decimal(
            ''.join(['9'] * int_digits) + ('.' + ''.join(['9'] * fraction_digits) if fraction_digits else '')
        )

    @staticmethod
    def _get_min_possible_value(total_digits: int, fraction_digits: int) -> Decimal:
        int_digits: int = total_digits - fraction_digits
        return Decimal(
            '-' + ''.join(['9'] * int_digits) + ('.' + ''.join(['9'] * fraction_digits) if fraction_digits else '')
        )
