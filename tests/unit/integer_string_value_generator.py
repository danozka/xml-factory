import pytest

from xml_factory.domain.base_type import BaseType
from xml_factory.domain.restriction import Restriction
from xml_factory.simple.integer_string_value_generator import IntegerStringValueGenerator


@pytest.fixture
def generator() -> IntegerStringValueGenerator:
    return IntegerStringValueGenerator()


def test_generate_max_integer_string_value_inclusive(generator: IntegerStringValueGenerator) -> None:
    restriction: Restriction = Restriction(base_type=BaseType(BaseType.integer), max_inclusive=7)
    value: str = generator.generate_max_integer_string_value(restriction)
    assert value == '7'


def test_generate_max_integer_string_value_exclusive(generator: IntegerStringValueGenerator) -> None:
    restriction: Restriction = Restriction(base_type=BaseType(BaseType.integer), max_exclusive=6)
    value: str = generator.generate_max_integer_string_value(restriction)
    assert value == '5'


def test_generate_max_integer_string_value_default(generator: IntegerStringValueGenerator) -> None:
    restriction: Restriction = Restriction(base_type=BaseType(BaseType.integer))
    value: str = generator.generate_max_integer_string_value(restriction)
    assert generator.RANDOM_MIN_INTEGER <= int(value) <= generator.RANDOM_MAX_INTEGER


def test_generate_min_integer_string_value_inclusive(generator: IntegerStringValueGenerator) -> None:
    restriction: Restriction = Restriction(base_type=BaseType(BaseType.integer), min_inclusive=2)
    value: str = generator.generate_min_integer_string_value(restriction)
    assert value == '2'


def test_generate_min_integer_string_value_exclusive(generator: IntegerStringValueGenerator) -> None:
    restriction: Restriction = Restriction(base_type=BaseType(BaseType.integer), min_exclusive=2)
    value: str = generator.generate_min_integer_string_value(restriction)
    assert value == '3'


def test_generate_random_integer_string_value_with_digits(generator: IntegerStringValueGenerator) -> None:
    restriction: Restriction = Restriction(
        base_type=BaseType(BaseType.integer),
        min_inclusive=10,
        max_inclusive=9999,
        total_digits=2
    )
    value: str = generator.generate_random_integer_string_value(restriction)
    assert 10 <= int(value) <= 99
    assert len(value) <= 2


def test_generate_random_integer_string_value_limits_swapped(generator: IntegerStringValueGenerator) -> None:
    restriction: Restriction = Restriction(base_type=BaseType(BaseType.integer), min_inclusive=10, max_inclusive=5)
    value: str = generator.generate_random_integer_string_value(restriction)
    assert value == '10'


def test_generate_random_integer_string_value_exclusive_range(generator: IntegerStringValueGenerator) -> None:
    restriction: Restriction = Restriction(base_type=BaseType(BaseType.integer), min_exclusive=2, max_exclusive=6)
    value: str = generator.generate_random_integer_string_value(restriction)
    min_value: int = 3
    max_value: int = 5
    int_value: int = int(value)
    assert min_value <= int_value <= max_value
