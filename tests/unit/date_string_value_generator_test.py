from datetime import timedelta
from unittest.mock import MagicMock, patch

import pytest
from elementpath.datatypes import Date10, Timezone

from xml_factory.domain.base_type import BaseType
from xml_factory.domain.restriction import Restriction
from xml_factory.simple.date_string_value_generator import DateStringValueGenerator


@pytest.fixture
def generator() -> DateStringValueGenerator:
    return DateStringValueGenerator()


def test_generate_max_date_string_value_with_max_inclusive(generator: DateStringValueGenerator) -> None:
    max_date: Date10 = Date10(year=2023, month=12, day=31)
    restriction: Restriction = Restriction(base_type=BaseType(BaseType.date), max_inclusive=max_date)
    result: str = generator.generate_max_date_string_value(restriction)
    assert result == str(max_date)


def test_generate_max_date_string_value_with_max_exclusive(generator: DateStringValueGenerator) -> None:
    max_date: Date10 = Date10(year=2023, month=12, day=31)
    expected_date: Date10 = Date10(year=2023, month=12, day=30)
    restriction: Restriction = Restriction(base_type=BaseType(BaseType.date), max_exclusive=max_date)
    result: str = generator.generate_max_date_string_value(restriction)
    assert result == str(expected_date)


def test_generate_max_date_string_value_without_max_restrictions(generator: DateStringValueGenerator) -> None:
    restriction: Restriction = Restriction(base_type=BaseType(BaseType.date))
    mock: MagicMock
    with patch.object(
        target=generator, 
        attribute='generate_random_date_string_value', 
        return_value='2023-01-01'
    ) as mock:
        result: str = generator.generate_max_date_string_value(restriction)
        assert result == '2023-01-01'
        mock.assert_called_once_with(restriction)


def test_generate_min_date_string_value_with_min_inclusive(generator: DateStringValueGenerator) -> None:
    min_date: Date10 = Date10(year=2023, month=1, day=1)
    restriction: Restriction = Restriction(base_type=BaseType(BaseType.date), min_inclusive=min_date)
    result: str = generator.generate_min_date_string_value(restriction)
    assert result == str(min_date)


def test_generate_min_date_string_value_with_min_exclusive(generator: DateStringValueGenerator) -> None:
    min_date: Date10 = Date10(year=2023, month=1, day=1)
    expected_date = Date10(year=2023, month=1, day=2)
    restriction: Restriction = Restriction(base_type=BaseType(BaseType.date), min_exclusive=min_date)
    result: str = generator.generate_min_date_string_value(restriction)
    assert result == str(expected_date)


def test_generate_min_date_string_value_without_min_restrictions(generator: DateStringValueGenerator) -> None:
    restriction: Restriction = Restriction(base_type=BaseType(BaseType.date))
    mock: MagicMock
    with patch.object(
        target=generator,
        attribute='generate_random_date_string_value',
        return_value='2023-01-01'
    ) as mock:
        result: str = generator.generate_min_date_string_value(restriction)
        assert result == '2023-01-01'
        mock.assert_called_once_with(restriction)


def test_generate_random_date_string_value_with_inclusive_bounds(generator: DateStringValueGenerator) -> None:
    min_date: Date10 = Date10(year=2023, month=1, day=1)
    max_date: Date10 = Date10(year=2023, month=1, day=10)
    restriction: Restriction = Restriction(
        base_type=BaseType(BaseType.date),
        min_inclusive=min_date,
        max_inclusive=max_date
    )
    result: str = generator.generate_random_date_string_value(restriction)
    result_date: Date10 = Date10.fromstring(result)
    assert min_date <= result_date <= max_date


def test_generate_random_date_string_value_with_exclusive_bounds(generator: DateStringValueGenerator) -> None:
    min_date: Date10 = Date10(year=2023, month=1, day=1)
    max_date: Date10 = Date10(year=2023, month=1, day=10)
    restriction: Restriction = Restriction(
        base_type=BaseType(BaseType.date),
        min_exclusive=min_date,
        max_exclusive=max_date
    )
    result: str = generator.generate_random_date_string_value(restriction)
    result_date: Date10 = Date10.fromstring(result)
    assert min_date < result_date < max_date


def test_generate_random_date_string_value_without_restrictions(generator: DateStringValueGenerator) -> None:
    restriction: Restriction = Restriction(base_type=BaseType(BaseType.date))
    result: str = generator.generate_random_date_string_value(restriction)
    result_date = Date10.fromstring(result)
    assert generator.RANDOM_MIN_DATE <= result_date <= generator.RANDOM_MAX_DATE


def test_generate_random_date_string_value_with_min_greater_than_max(generator: DateStringValueGenerator) -> None:
    min_date: Date10 = Date10(year=2023, month=1, day=10)
    max_date: Date10 = Date10(year=2023, month=1, day=1)
    restriction: Restriction = Restriction(
        base_type=BaseType(BaseType.date),
        min_inclusive=min_date,
        max_inclusive=max_date
    )
    result: str = generator.generate_random_date_string_value(restriction)
    assert result == str(min_date)


def test_generate_random_date_string_value_preserves_timezone(generator: DateStringValueGenerator) -> None:
    tz: Timezone = Timezone(timedelta(hours=0))
    min_date: Date10 = Date10(year=2023, month=1, day=1, tzinfo=tz)
    restriction: Restriction = Restriction(base_type=BaseType(BaseType.date), min_inclusive=min_date)
    result: str = generator.generate_random_date_string_value(restriction)
    result_date: Date10 = Date10.fromstring(result)
    assert result_date.tzinfo is not None
    assert result_date.tzinfo == tz


def test_generate_random_date_string_value_mixed_bounds(generator: DateStringValueGenerator) -> None:
    min_date: Date10 = Date10(year=2023, month=1, day=1)
    max_date: Date10 = Date10(year=2023, month=1, day=10)
    restriction: Restriction = Restriction(
        base_type=BaseType(BaseType.date),
        min_inclusive=min_date,
        max_exclusive=max_date
    )
    result: str = generator.generate_random_date_string_value(restriction)
    result_date: Date10 = Date10.fromstring(result)
    assert min_date <= result_date < max_date
