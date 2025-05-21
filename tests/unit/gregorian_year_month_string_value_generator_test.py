from datetime import timedelta

import pytest
from elementpath.datatypes import GregorianYearMonth10, Timezone

from xml_factory.domain.base_type import BaseType
from xml_factory.domain.restriction import Restriction
from xml_factory.simple.gregorian_year_month_value_generator import GregorianYearMonthStringValueGenerator


@pytest.fixture
def generator() -> GregorianYearMonthStringValueGenerator:
    return GregorianYearMonthStringValueGenerator()


def test_generate_max_gregorian_year_month_string_value_max_inclusive(
    generator: GregorianYearMonthStringValueGenerator
) -> None:
    restriction: Restriction = Restriction(
        base_type=BaseType(BaseType.gregorian_year_month),
        max_inclusive=GregorianYearMonth10(year=2023, month=5)
    )
    result: str = generator.generate_max_gregorian_year_month_string_value(restriction)
    assert result == '2023-05'


def test_generate_max_gregorian_year_month_string_value_max_exclusive(
    generator: GregorianYearMonthStringValueGenerator
) -> None:
    restriction: Restriction = Restriction(
        base_type=BaseType(BaseType.gregorian_year_month),
        max_exclusive=GregorianYearMonth10(year=2023, month=6)
    )
    result: str = generator.generate_max_gregorian_year_month_string_value(restriction)
    assert result == '2023-05'


def test_generate_min_gregorian_year_month_string_value_min_inclusive(
    generator: GregorianYearMonthStringValueGenerator
) -> None:
    restriction: Restriction = Restriction(
        base_type=BaseType(BaseType.gregorian_year_month),
        min_inclusive=GregorianYearMonth10(year=2023, month=3)
    )
    result: str = generator.generate_min_gregorian_year_month_string_value(restriction)
    assert result == '2023-03'


def test_generate_min_gregorian_year_month_string_value_min_exclusive(
    generator: GregorianYearMonthStringValueGenerator
) -> None:
    restriction: Restriction = Restriction(
        base_type=BaseType(BaseType.gregorian_year_month),
        min_exclusive=GregorianYearMonth10(year=2023, month=4)
    )
    result: str = generator.generate_min_gregorian_year_month_string_value(restriction)
    assert result == '2023-05'


def test_generate_min_gregorian_year_month_string_value_min_exclusive_december(
    generator: GregorianYearMonthStringValueGenerator
) -> None:
    restriction: Restriction = Restriction(
        base_type=BaseType(BaseType.gregorian_year_month),
        min_exclusive=GregorianYearMonth10(year=2023, month=12)
    )
    result: str = generator.generate_min_gregorian_year_month_string_value(restriction)
    assert result == '2024-01'


def test_generate_max_gregorian_year_month_string_value_max_exclusive_january(
    generator: GregorianYearMonthStringValueGenerator
) -> None:
    restriction: Restriction = Restriction(
        base_type=BaseType(BaseType.gregorian_year_month),
        max_exclusive=GregorianYearMonth10(year=2023, month=1)
    )
    result: str = generator.generate_max_gregorian_year_month_string_value(restriction)
    assert result == '2022-12'


def test_generate_random_gregorian_year_month_string_value_no_restrictions(
    generator: GregorianYearMonthStringValueGenerator
) -> None:
    restriction: Restriction = Restriction(base_type=BaseType(BaseType.gregorian_year_month))
    result: str = generator.generate_random_gregorian_year_month_string_value(restriction)
    parts: list[str] = result.split('-')
    year: int = int(parts[0])
    month: int = int(parts[1])
    assert generator.RANDOM_MIN_GREGORIAN_YEAR_MONTH.year <= year <= generator.RANDOM_MAX_GREGORIAN_YEAR_MONTH.year
    assert 1 <= month <= 12


def test_generate_random_gregorian_year_month_string_value_with_tz(
    generator: GregorianYearMonthStringValueGenerator
) -> None:
    tz: Timezone = Timezone(timedelta(hours=5))
    restriction: Restriction = Restriction(
        base_type=BaseType(BaseType.gregorian_year_month),
        min_inclusive=GregorianYearMonth10(year=2023, month=2, tzinfo=tz)
    )
    result: str = generator.generate_random_gregorian_year_month_string_value(restriction)
    assert '+05:00' in result or 'Z' in result


def test_max_less_than_min(generator: GregorianYearMonthStringValueGenerator) -> None:
    restriction: Restriction = Restriction(
        base_type=BaseType(BaseType.gregorian_year_month),
        min_inclusive=GregorianYearMonth10(year=2023, month=8),
        max_inclusive=GregorianYearMonth10(year=2022, month=5)
    )
    result: str = generator.generate_random_gregorian_year_month_string_value(restriction)
    assert result == '2023-08'
