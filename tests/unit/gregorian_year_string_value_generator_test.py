from datetime import timedelta

import pytest
from elementpath.datatypes import GregorianYear10, Timezone

from xml_factory.domain.base_type import BaseType
from xml_factory.domain.restriction import Restriction
from xml_factory.simple.gregorian_year_string_value_generator import GregorianYearStringValueGenerator


@pytest.fixture
def generator() -> GregorianYearStringValueGenerator:
    return GregorianYearStringValueGenerator()


def test_generate_max_gregorian_year_string_value_max_inclusive(generator: GregorianYearStringValueGenerator) -> None:
    restriction: Restriction = Restriction(
        name='gYearTest',
        base_type=BaseType(BaseType.gregorian_year),
        max_inclusive=GregorianYear10(year=2023)
    )
    result: str = generator.generate_max_gregorian_year_string_value(restriction)
    assert result == '2023'


def test_generate_max_gregorian_year_string_value_max_exclusive(generator: GregorianYearStringValueGenerator) -> None:
    restriction: Restriction = Restriction(
        name='gYearTest',
        base_type=BaseType(BaseType.gregorian_year),
        max_exclusive=GregorianYear10(year=2023)
    )
    result: str = generator.generate_max_gregorian_year_string_value(restriction)
    assert result == '2022'


def test_generate_min_gregorian_year_string_value_min_inclusive(generator: GregorianYearStringValueGenerator) -> None:
    restriction: Restriction = Restriction(
        name='gYearTest',
        base_type=BaseType(BaseType.gregorian_year),
        min_inclusive=GregorianYear10(year=1995)
    )
    result: str = generator.generate_min_gregorian_year_string_value(restriction)
    assert result == '1995'


def test_generate_min_gregorian_year_string_value_min_exclusive(generator: GregorianYearStringValueGenerator) -> None:
    restriction: Restriction = Restriction(
        name='gYearTest',
        base_type=BaseType(BaseType.gregorian_year),
        min_exclusive=GregorianYear10(year=1995)
    )
    result: str = generator.generate_min_gregorian_year_string_value(restriction)
    assert result == '1996'


def test_generate_random_gregorian_year_string_value_no_restrictions(
    generator: GregorianYearStringValueGenerator
) -> None:
    restriction: Restriction = Restriction(name='gYearTest', base_type=BaseType(BaseType.gregorian_year))
    result: str = generator.generate_random_gregorian_year_string_value(restriction)
    year: int = int(result)
    assert generator.RANDOM_MIN_GREGORIAN_YEAR.year <= year <= generator.RANDOM_MAX_GREGORIAN_YEAR.year


def test_generate_random_gregorian_year_string_value_with_tz(generator: GregorianYearStringValueGenerator) -> None:
    tz: Timezone = Timezone(timedelta(hours=5))
    restriction: Restriction = Restriction(
        name='gYearTest',
        base_type=BaseType(BaseType.gregorian_year),
        min_inclusive=GregorianYear10(year=2010, tzinfo=tz)
    )
    result: str = generator.generate_random_gregorian_year_string_value(restriction)
    assert '+05:00' in result or 'Z' in result


def test_max_less_than_min(generator: GregorianYearStringValueGenerator) -> None:
    restriction: Restriction = Restriction(
        name='gYearTest',
        base_type=BaseType(BaseType.gregorian_year),
        min_inclusive=GregorianYear10(year=2022),
        max_inclusive=GregorianYear10(year=2010)
    )
    result: str = generator.generate_random_gregorian_year_string_value(restriction)
    assert result == '2022'