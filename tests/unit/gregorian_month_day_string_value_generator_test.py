from datetime import timedelta

import pytest
from elementpath.datatypes import GregorianMonthDay, Timezone

from xml_factory.domain.base_type import BaseType
from xml_factory.domain.restriction import Restriction
from xml_factory.simple.gregorian_month_day_string_value_generator import GregorianMonthDayStringValueGenerator


@pytest.fixture
def generator() -> GregorianMonthDayStringValueGenerator:
    return GregorianMonthDayStringValueGenerator()


def test_generate_max_gregorian_month_day_string_value_max_inclusive(
    generator: GregorianMonthDayStringValueGenerator
) -> None:
    restriction: Restriction = Restriction(
        name='gMonthDayTest',
        base_type=BaseType(BaseType.gregorian_month_day),
        max_inclusive=GregorianMonthDay(month=5, day=15)
    )
    result: str = generator.generate_max_gregorian_month_day_string_value(restriction)
    assert result == '--05-15'


def test_generate_max_gregorian_month_day_string_value_max_exclusive(
    generator: GregorianMonthDayStringValueGenerator
) -> None:
    restriction: Restriction = Restriction(
        name='gMonthDayTest',
        base_type=BaseType(BaseType.gregorian_month_day),
        max_exclusive=GregorianMonthDay(month=6, day=20)
    )
    result: str = generator.generate_max_gregorian_month_day_string_value(restriction)
    assert result == '--06-19'


def test_generate_min_gregorian_month_day_string_value_min_inclusive(
    generator: GregorianMonthDayStringValueGenerator
) -> None:
    restriction: Restriction = Restriction(
        name='gMonthDayTest',
        base_type=BaseType(BaseType.gregorian_month_day),
        min_inclusive=GregorianMonthDay(month=3, day=4)
    )
    result: str = generator.generate_min_gregorian_month_day_string_value(restriction)
    assert result == '--03-04'


def test_generate_min_gregorian_month_day_string_value_min_exclusive(
    generator: GregorianMonthDayStringValueGenerator
) -> None:
    restriction: Restriction = Restriction(
        name='gMonthDayTest',
        base_type=BaseType(BaseType.gregorian_month_day),
        min_exclusive=GregorianMonthDay(month=4, day=6)
    )
    result: str = generator.generate_min_gregorian_month_day_string_value(restriction)
    assert result == '--04-07'


def test_generate_random_gregorian_month_day_string_value_no_restrictions(
    generator: GregorianMonthDayStringValueGenerator
) -> None:
    restriction: Restriction = Restriction(name='gMonthDayTest', base_type=BaseType(BaseType.gregorian_month_day))
    result: str = generator.generate_random_gregorian_month_day_string_value(restriction)
    assert result.startswith('--')
    parts: list[str] = result.split('-')
    month: int = int(parts[2])
    day: int = int(parts[3])
    assert 1 <= month <= 12
    assert 1 <= day <= 31
    if month == 2:
        assert day <= 29
    elif month in {4, 6, 9, 11}:
        assert day <= 30
    else:
        assert day <= 31


def test_generate_random_gregorian_month_day_string_value_with_tz(
    generator: GregorianMonthDayStringValueGenerator
) -> None:
    tz: Timezone = Timezone(timedelta(hours=5))
    restriction: Restriction = Restriction(
        name='gMonthDayTest',
        base_type=BaseType(BaseType.gregorian_month_day),
        min_inclusive=GregorianMonthDay(month=2, day=10, tzinfo=tz)
    )
    result: str = generator.generate_random_gregorian_month_day_string_value(restriction)
    assert '+05:00' in result or 'Z' in result


def test_max_less_than_min(generator: GregorianMonthDayStringValueGenerator) -> None:
    restriction: Restriction = Restriction(
        name='gMonthDayTest',
        base_type=BaseType(BaseType.gregorian_month_day),
        min_inclusive=GregorianMonthDay(month=5, day=21),
        max_inclusive=GregorianMonthDay(month=4, day=12)
    )
    result: str = generator.generate_random_gregorian_month_day_string_value(restriction)
    assert result == '--05-21'
