from datetime import timedelta

import pytest
from elementpath.datatypes import GregorianMonth, Timezone

from xml_factory.domain.base_type import BaseType
from xml_factory.domain.restriction import Restriction
from xml_factory.simple.gregorian_month_string_value_generator import GregorianMonthStringValueGenerator


@pytest.fixture
def generator() -> GregorianMonthStringValueGenerator:
    return GregorianMonthStringValueGenerator()


def test_generate_max_gregorian_month_string_value_max_inclusive(generator: GregorianMonthStringValueGenerator) -> None:
    restriction: Restriction = Restriction(
        base_type=BaseType(BaseType.gregorian_month),
        max_inclusive=GregorianMonth(month=5)
    )
    result: str = generator.generate_max_gregorian_month_string_value(restriction)
    assert result == '--05'


def test_generate_max_gregorian_month_string_value_max_exclusive(generator: GregorianMonthStringValueGenerator) -> None:
    restriction: Restriction = Restriction(
        base_type=BaseType(BaseType.gregorian_month),
        max_exclusive=GregorianMonth(month=6)
    )
    result: str = generator.generate_max_gregorian_month_string_value(restriction)
    assert result == '--05'


def test_generate_min_gregorian_month_string_value_min_inclusive(generator: GregorianMonthStringValueGenerator) -> None:
    restriction: Restriction = Restriction(
        base_type=BaseType(BaseType.gregorian_month),
        min_inclusive=GregorianMonth(month=3)
    )
    result: str = generator.generate_min_gregorian_month_string_value(restriction)
    assert result == '--03'


def test_generate_min_gregorian_month_string_value_min_exclusive(generator: GregorianMonthStringValueGenerator) -> None:
    restriction: Restriction = Restriction(
        base_type=BaseType(BaseType.gregorian_month),
        min_exclusive=GregorianMonth(month=4)
    )
    result: str = generator.generate_min_gregorian_month_string_value(restriction)
    assert result == '--05'


def test_generate_random_gregorian_month_string_value_no_restrictions(
    generator: GregorianMonthStringValueGenerator
) -> None:
    restriction: Restriction = Restriction(base_type=BaseType(BaseType.gregorian_month))
    result: str = generator.generate_random_gregorian_month_string_value(restriction)
    assert result.startswith('--')
    month: int = int(result[2:])
    assert 1 <= month <= 12


def test_generate_random_gregorian_month_string_value_with_tz(generator: GregorianMonthStringValueGenerator) -> None:
    tz: Timezone = Timezone(timedelta(hours=5))
    restriction: Restriction = Restriction(
        base_type=BaseType(BaseType.gregorian_month),
        min_inclusive=GregorianMonth(month=2, tzinfo=tz)
    )
    result: str = generator.generate_random_gregorian_month_string_value(restriction)
    assert '+05:00' in result or 'Z' in result


def test_max_less_than_min(generator: GregorianMonthStringValueGenerator) -> None:
    restriction: Restriction = Restriction(
        base_type=BaseType(BaseType.gregorian_month),
        min_inclusive=GregorianMonth(month=8),
        max_inclusive=GregorianMonth(month=5)
    )
    result: str = generator.generate_random_gregorian_month_string_value(restriction)
    assert result == '--08'
