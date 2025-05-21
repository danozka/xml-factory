import pytest

from xml_factory.domain.base_type import BaseType
from xml_factory.domain.restriction import Restriction
from xml_factory.simple.string_value_generator import StringValueGenerator


@pytest.fixture
def generator() -> StringValueGenerator:
    return StringValueGenerator()


def test_specific_length_string_is_correct(generator: StringValueGenerator) -> None:
    length: int = 12
    value: str = generator.generate_specific_length_string_value(length)
    assert len(value) == length


def test_random_string_with_exact_length_restriction(generator: StringValueGenerator) -> None:
    restriction: Restriction = Restriction(base_type=BaseType(BaseType.string), length=10)
    value: str = generator.generate_random_string_value(restriction)
    assert len(value) == 10


def test_random_string_with_min_length_restriction(generator: StringValueGenerator) -> None:
    min_length: int = 14
    restriction: Restriction = Restriction(base_type=BaseType(BaseType.string), min_length=min_length)
    value: str = generator.generate_random_string_value(restriction)
    assert len(value) >= min_length


def test_random_string_with_max_length_restriction(generator: StringValueGenerator) -> None:
    max_length: int = 9
    restriction: Restriction = Restriction(base_type=BaseType(BaseType.string), max_length=max_length)
    value: str = generator.generate_random_string_value(restriction)
    assert len(value) <= max_length


def test_random_string_with_min_and_max_length(generator: StringValueGenerator) -> None:
    min_length: int = 6
    max_length: int = 13
    restriction: Restriction = Restriction(
        base_type=BaseType(BaseType.string),
        min_length=min_length,
        max_length=max_length
    )
    value: str = generator.generate_random_string_value(restriction)
    assert min_length <= len(value) <= max_length


def test_random_string_invalid_max_smaller_than_min(generator: StringValueGenerator) -> None:
    min_length: int = 8
    max_length: int = 4
    restriction: Restriction = Restriction(
        base_type=BaseType(BaseType.string),
        min_length=min_length,
        max_length=max_length
    )
    value: str = generator.generate_random_string_value(restriction)
    assert len(value) == min_length


def test_default_length_boundaries_when_not_specified(generator: StringValueGenerator) -> None:
    restriction: Restriction = Restriction(base_type=BaseType(BaseType.string))
    value: str = generator.generate_random_string_value(restriction)
    assert generator.RANDOM_MIN_LENGTH <= len(value) <= generator.RANDOM_MAX_LENGTH
