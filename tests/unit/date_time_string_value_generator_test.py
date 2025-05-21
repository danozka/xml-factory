from datetime import timedelta
from unittest.mock import MagicMock, patch

import pytest
from elementpath.datatypes import DateTime10, Timezone

from xml_factory.domain.base_type import BaseType
from xml_factory.domain.restriction import Restriction
from xml_factory.simple.date_time_string_value_generator import DateTimeStringValueGenerator


@pytest.fixture
def generator() -> DateTimeStringValueGenerator:
    return DateTimeStringValueGenerator()


def test_generate_max_date_time_string_value_with_max_inclusive(generator: DateTimeStringValueGenerator) -> None:
    max_dt: DateTime10 = DateTime10(year=2023, month=12, day=31, hour=13, minute=0, second=0)
    restriction: Restriction = Restriction(base_type=BaseType(BaseType.date_time), max_inclusive=max_dt)
    result: str = generator.generate_max_date_time_string_value(restriction)
    assert result == str(max_dt)


def test_generate_max_date_time_string_value_with_max_exclusive(generator: DateTimeStringValueGenerator) -> None:
    max_dt: DateTime10 = DateTime10(year=2023, month=12, day=31, hour=23, minute=59, second=59, microsecond=123456)
    expected: DateTime10 = DateTime10(year=2023, month=12, day=31, hour=23, minute=59, second=59, microsecond=123455)
    restriction: Restriction = Restriction(base_type=BaseType(BaseType.date_time), max_exclusive=max_dt)
    result: str = generator.generate_max_date_time_string_value(restriction)
    assert result == str(expected)


def test_generate_max_date_time_string_value_without_max_restrictions(generator: DateTimeStringValueGenerator) -> None:
    restriction: Restriction = Restriction(base_type=BaseType(BaseType.date_time))
    mock: MagicMock
    with patch.object(
        target=generator,
        attribute='generate_random_date_time_string_value', 
        return_value='2022-08-15T10:00:00'
    ) as mock:
        result: str = generator.generate_max_date_time_string_value(restriction)
        assert result == '2022-08-15T10:00:00'
        mock.assert_called_once_with(restriction)


def test_generate_min_date_time_string_value_with_min_inclusive(generator: DateTimeStringValueGenerator) -> None:
    min_dt: DateTime10 = DateTime10(year=2020, month=1, day=1, hour=0, minute=30, second=0)
    restriction: Restriction = Restriction(base_type=BaseType(BaseType.date_time), min_inclusive=min_dt)
    result: str = generator.generate_min_date_time_string_value(restriction)
    assert result == str(min_dt)


def test_generate_min_date_time_string_value_with_min_exclusive(generator: DateTimeStringValueGenerator) -> None:
    min_dt: DateTime10 = DateTime10(year=2020, month=1, day=1, hour=0, minute=0, second=0, microsecond=999999)
    expected: DateTime10 = DateTime10(year=2020, month=1, day=1, hour=0, minute=0, second=1, microsecond=0)
    restriction: Restriction = Restriction(base_type=BaseType(BaseType.date_time), min_exclusive=min_dt)
    result: str = generator.generate_min_date_time_string_value(restriction)
    assert result == str(expected)


def test_generate_min_date_time_string_value_without_min_restrictions(generator: DateTimeStringValueGenerator) -> None:
    restriction: Restriction = Restriction(base_type=BaseType(BaseType.date_time))
    mock: MagicMock
    with patch.object(
        target=generator,
        attribute='generate_random_date_time_string_value',
        return_value='1911-05-03T12:00:11'
    ) as mock:
        result: str = generator.generate_min_date_time_string_value(restriction)
        assert result == '1911-05-03T12:00:11'
        mock.assert_called_once_with(restriction)


def test_generate_random_date_time_string_value_with_inclusive_bounds(generator: DateTimeStringValueGenerator) -> None:
    min_dt: DateTime10 = DateTime10(year=2022, month=6, day=1, hour=8, minute=30, second=0)
    max_dt: DateTime10 = DateTime10(year=2022, month=6, day=1, hour=18, minute=0, second=0)
    restriction: Restriction = Restriction(
        base_type=BaseType(BaseType.date_time),
        min_inclusive=min_dt,
        max_inclusive=max_dt
    )
    result: str = generator.generate_random_date_time_string_value(restriction)
    result_dt: DateTime10 = DateTime10.fromstring(result)
    assert min_dt <= result_dt <= max_dt


def test_generate_random_date_time_string_value_with_exclusive_bounds(generator: DateTimeStringValueGenerator) -> None:
    min_dt: DateTime10 = DateTime10(year=2022, month=6, day=1, hour=8, minute=0, second=0)
    max_dt: DateTime10 = DateTime10(year=2022, month=6, day=1, hour=20, minute=0, second=0)
    restriction: Restriction = Restriction(
        base_type=BaseType(BaseType.date_time),
        min_exclusive=min_dt,
        max_exclusive=max_dt
    )
    result: str = generator.generate_random_date_time_string_value(restriction)
    result_dt: DateTime10 = DateTime10.fromstring(result)
    assert min_dt < result_dt < max_dt


def test_generate_random_date_time_string_value_without_restrictions(generator: DateTimeStringValueGenerator) -> None:
    restriction: Restriction = Restriction(base_type=BaseType(BaseType.date_time))
    result: str = generator.generate_random_date_time_string_value(restriction)
    result_dt: DateTime10 = DateTime10.fromstring(result)
    assert generator.RANDOM_MIN_DATE_TIME <= result_dt <= generator.RANDOM_MAX_DATE_TIME


def test_generate_random_date_time_string_value_with_min_greater_than_max(
    generator: DateTimeStringValueGenerator
) -> None:
    min_dt: DateTime10 = DateTime10(year=2023, month=10, day=2, hour=12, minute=0, second=0)
    max_dt: DateTime10 = DateTime10(year=2023, month=5, day=1, hour=1, minute=0, second=0)
    restriction: Restriction = Restriction(
        base_type=BaseType(BaseType.date_time),
        min_inclusive=min_dt,
        max_inclusive=max_dt
    )
    result: str = generator.generate_random_date_time_string_value(restriction)
    assert result == str(min_dt)


def test_generate_random_date_time_string_value_preserves_timezone(generator: DateTimeStringValueGenerator) -> None:
    tz: Timezone = Timezone(timedelta(hours=1))
    min_dt: DateTime10 = DateTime10(year=2023, month=1, day=1, hour=8, minute=0, second=0, tzinfo=tz)
    restriction: Restriction = Restriction(base_type=BaseType(BaseType.date_time), min_inclusive=min_dt)
    result: str = generator.generate_random_date_time_string_value(restriction)
    result_dt: DateTime10 = DateTime10.fromstring(result)
    assert result_dt.tzinfo is not None
    assert result_dt.tzinfo == tz


def test_generate_random_date_time_string_value_mixed_bounds(generator: DateTimeStringValueGenerator) -> None:
    min_dt: DateTime10 = DateTime10(year=2022, month=6, day=1, hour=7, minute=0, second=0)
    max_dt: DateTime10 = DateTime10(year=2022, month=6, day=1, hour=17, minute=0, second=0)
    restriction: Restriction = Restriction(
        base_type=BaseType(BaseType.date_time),
        min_inclusive=min_dt,
        max_exclusive=max_dt
    )
    result: str = generator.generate_random_date_time_string_value(restriction)
    result_dt: DateTime10 = DateTime10.fromstring(result)
    assert min_dt <= result_dt < max_dt