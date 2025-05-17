from datetime import timedelta
from unittest.mock import MagicMock, patch

import pytest
from elementpath.datatypes import Time, Timezone

from xml_factory.domain.base_type import BaseType
from xml_factory.domain.restriction import Restriction
from xml_factory.simple.time_string_value_generator import TimeStringValueGenerator


@pytest.fixture
def generator() -> TimeStringValueGenerator:
    return TimeStringValueGenerator()


def test_generate_max_time_string_value_with_max_inclusive(generator: TimeStringValueGenerator) -> None:
    max_time: Time = Time(hour=21, minute=15, second=43)
    restriction: Restriction = Restriction(name='test', base_type=BaseType(BaseType.time), max_inclusive=max_time)
    result: str = generator.generate_max_time_string_value(restriction=restriction)
    assert result == str(max_time)


def test_generate_max_time_string_value_with_max_exclusive(generator: TimeStringValueGenerator) -> None:
    max_time: Time = Time(hour=22, minute=0, second=0, microsecond=300)
    expected: Time = Time(hour=22, minute=0, second=0, microsecond=299)
    restriction: Restriction = Restriction(name='test', base_type=BaseType(BaseType.time), max_exclusive=max_time)
    result: str = generator.generate_max_time_string_value(restriction=restriction)
    assert result == str(expected)


def test_generate_max_time_string_value_without_max_restrictions(generator: TimeStringValueGenerator) -> None:
    restriction: Restriction = Restriction(name='test', base_type=BaseType(BaseType.time))
    mock: MagicMock
    with patch.object(target=generator, attribute='generate_random_time_string_value', return_value='19:00:00') as mock:
        result: str = generator.generate_max_time_string_value(restriction=restriction)
        assert result == '19:00:00'
        mock.assert_called_once_with(restriction)


def test_generate_min_time_string_value_with_min_inclusive(generator: TimeStringValueGenerator) -> None:
    min_time: Time = Time(hour=6, minute=0, second=10)
    restriction: Restriction = Restriction(name='test', base_type=BaseType(BaseType.time), min_inclusive=min_time)
    result: str = generator.generate_min_time_string_value(restriction=restriction)
    assert result == str(min_time)


def test_generate_min_time_string_value_with_min_exclusive(generator: TimeStringValueGenerator) -> None:
    min_time: Time = Time(hour=5, minute=7, second=15, microsecond=999999)
    expected: Time = Time(hour=5, minute=7, second=16, microsecond=0)
    restriction: Restriction = Restriction(name='test', base_type=BaseType(BaseType.time), min_exclusive=min_time)
    result: str = generator.generate_min_time_string_value(restriction=restriction)
    assert result == str(expected)


def test_generate_min_time_string_value_without_min_restrictions(generator: TimeStringValueGenerator) -> None:
    restriction: Restriction = Restriction(name='test', base_type=BaseType(BaseType.time))
    mock: MagicMock
    with patch.object(target=generator, attribute='generate_random_time_string_value', return_value='11:11:11') as mock:
        result: str = generator.generate_min_time_string_value(restriction=restriction)
        assert result == '11:11:11'
        mock.assert_called_once_with(restriction)


def test_generate_random_time_string_value_with_inclusive_bounds(generator: TimeStringValueGenerator) -> None:
    min_time: Time = Time(hour=8, minute=30, second=0)
    max_time: Time = Time(hour=10, minute=0, second=0)
    restriction: Restriction = Restriction(
        name='test',
        base_type=BaseType(BaseType.time),
        min_inclusive=min_time,
        max_inclusive=max_time
    )
    result: str = generator.generate_random_time_string_value(restriction=restriction)
    result_time: Time = Time.fromstring(result)
    assert min_time <= result_time <= max_time


def test_generate_random_time_string_value_with_exclusive_bounds(generator: TimeStringValueGenerator) -> None:
    min_time: Time = Time(hour=7, minute=0, second=0)
    max_time: Time = Time(hour=12, minute=0, second=0)
    restriction: Restriction = Restriction(
        name='test',
        base_type=BaseType(BaseType.time),
        min_exclusive=min_time,
        max_exclusive=max_time
    )
    result: str = generator.generate_random_time_string_value(restriction=restriction)
    result_time: Time = Time.fromstring(result)
    assert min_time < result_time < max_time


def test_generate_random_time_string_value_without_restrictions(generator: TimeStringValueGenerator) -> None:
    restriction: Restriction = Restriction(name='test', base_type=BaseType(BaseType.time))
    result: str = generator.generate_random_time_string_value(restriction=restriction)
    result_time: Time = Time.fromstring(result)
    assert generator.RANDOM_MIN_TIME <= result_time <= generator.RANDOM_MAX_TIME


def test_generate_random_time_string_value_with_min_greater_than_max(generator: TimeStringValueGenerator) -> None:
    min_time: Time = Time(hour=14, minute=0, second=0)
    max_time: Time = Time(hour=11, minute=0, second=0)
    restriction: Restriction = Restriction(
        name='test',
        base_type=BaseType(BaseType.time),
        min_inclusive=min_time,
        max_inclusive=max_time
    )
    result: str = generator.generate_random_time_string_value(restriction=restriction)
    assert result == str(min_time)


def test_generate_random_time_string_value_preserves_timezone(generator: TimeStringValueGenerator) -> None:
    tz: Timezone = Timezone(timedelta(hours=3))
    min_time: Time = Time(hour=7, minute=0, second=0, tzinfo=tz)
    restriction: Restriction = Restriction(name='test', base_type=BaseType(BaseType.time), min_inclusive=min_time)
    result: str = generator.generate_random_time_string_value(restriction=restriction)
    result_time: Time = Time.fromstring(result)
    assert result_time.tzinfo is not None
    assert result_time.tzinfo == tz


def test_generate_random_time_string_value_mixed_bounds(generator: TimeStringValueGenerator) -> None:
    min_time: Time = Time(hour=7, minute=0, second=0)
    max_time: Time = Time(hour=17, minute=30, second=0)
    restriction: Restriction = Restriction(
        name='test',
        base_type=BaseType(BaseType.time),
        min_inclusive=min_time,
        max_exclusive=max_time
    )
    result: str = generator.generate_random_time_string_value(restriction=restriction)
    result_time: Time = Time.fromstring(result)
    assert min_time <= result_time < max_time
