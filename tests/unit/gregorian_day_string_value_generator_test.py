from datetime import timedelta

import pytest
from elementpath.datatypes import GregorianDay, Timezone

from xml_factory.domain.base_type import BaseType
from xml_factory.domain.restriction import Restriction
from xml_factory.simple.gregorian_day_string_value_generator import GregorianDayStringValueGenerator


@pytest.fixture
def generator() -> GregorianDayStringValueGenerator:
    return GregorianDayStringValueGenerator()


def test_generate_max_gregorian_day_string_value_max_inclusive(generator: GregorianDayStringValueGenerator) -> None:
    restriction = Restriction(base_type=BaseType(BaseType.gregorian_day), max_inclusive=GregorianDay(day=15))
    result: str = generator.generate_max_gregorian_day_string_value(restriction)
    assert result == '---15'


def test_generate_max_gregorian_day_string_value_max_exclusive(generator: GregorianDayStringValueGenerator) -> None:
    restriction = Restriction(base_type=BaseType(BaseType.gregorian_day), max_exclusive=GregorianDay(day=20))
    result: str = generator.generate_max_gregorian_day_string_value(restriction)
    assert result == '---19'


def test_generate_min_gregorian_day_string_value_min_inclusive(generator: GregorianDayStringValueGenerator) -> None:
    restriction = Restriction(base_type=BaseType(BaseType.gregorian_day), min_inclusive=GregorianDay(day=4))
    result: str = generator.generate_min_gregorian_day_string_value(restriction)
    assert result == '---04'


def test_generate_min_gregorian_day_string_value_min_exclusive(generator: GregorianDayStringValueGenerator) -> None:
    restriction = Restriction(base_type=BaseType(BaseType.gregorian_day), min_exclusive=GregorianDay(day=6))
    result: str = generator.generate_min_gregorian_day_string_value(restriction)
    assert result == '---07'


def test_generate_random_gregorian_day_string_value_no_restrictions(
    generator: GregorianDayStringValueGenerator
) -> None:
    restriction = Restriction(base_type=BaseType(BaseType.gregorian_day))
    result: str = generator.generate_random_gregorian_day_string_value(restriction)
    assert result.startswith('---')
    day: int = int(result[3:5])
    assert 1 <= day <= 31


def test_generate_random_gregorian_day_string_value_with_tz(generator: GregorianDayStringValueGenerator) -> None:
    tz: Timezone = Timezone(timedelta(hours=5))
    restriction = Restriction(base_type=BaseType(BaseType.gregorian_day), min_inclusive=GregorianDay(day=10, tzinfo=tz))
    result: str = generator.generate_random_gregorian_day_string_value(restriction)
    assert '+05:00' in result or 'Z' in result


def test_max_less_than_min(
    generator: GregorianDayStringValueGenerator
) -> None:
    restriction = Restriction(
        base_type=BaseType(BaseType.gregorian_day),
        min_inclusive=GregorianDay(day=21),
        max_inclusive=GregorianDay(day=12)
    )
    result: str = generator.generate_random_gregorian_day_string_value(restriction)
    assert result == '---21'