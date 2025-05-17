from decimal import Decimal

import pytest

from xml_factory.domain.base_type import BaseType
from xml_factory.domain.restriction import Restriction
from xml_factory.simple.decimal_string_value_generator import DecimalStringValueGenerator


@pytest.fixture
def generator() -> DecimalStringValueGenerator:
    return DecimalStringValueGenerator()


def test_generate_max_decimal_string_value_simple(generator: DecimalStringValueGenerator) -> None:
    restriction: Restriction = Restriction(
        name='test',
        base_type=BaseType(BaseType.decimal),
        total_digits=5,
        fraction_digits=2
    )
    result: str = generator.generate_max_decimal_string_value(restriction)
    assert Decimal(result) == Decimal('999.99')


def test_generate_max_decimal_string_value_with_max_inclusive(generator: DecimalStringValueGenerator) -> None:
    restriction: Restriction = Restriction(
        name='test',
        base_type=BaseType(BaseType.decimal),
        total_digits=4,
        fraction_digits=1,
        max_inclusive=55.6
    )
    result: str = generator.generate_max_decimal_string_value(restriction)
    assert Decimal(result) == Decimal('55.6')


def test_generate_max_decimal_string_value_with_max_exclusive(generator: DecimalStringValueGenerator) -> None:
    restriction: Restriction = Restriction(
        name='test',
        base_type=BaseType(BaseType.decimal),
        total_digits=4,
        fraction_digits=1,
        max_exclusive=55.6
    )
    result: str = generator.generate_max_decimal_string_value(restriction)
    assert Decimal(result) == Decimal('55.5')


def test_generate_min_decimal_string_value_simple(generator: DecimalStringValueGenerator) -> None:
    restriction: Restriction = Restriction(
        name='test',
        base_type=BaseType(BaseType.decimal),
        total_digits=4,
        fraction_digits=2
    )
    result: str = generator.generate_min_decimal_string_value(restriction)
    assert Decimal(result) == Decimal('-99.99')


def test_generate_min_decimal_string_value_with_min_inclusive(generator: DecimalStringValueGenerator) -> None:
    restriction: Restriction = Restriction(
        name='test',
        base_type=BaseType(BaseType.decimal),
        total_digits=3,
        fraction_digits=0,
        min_inclusive=-10.0
    )
    result: str = generator.generate_min_decimal_string_value(restriction)
    assert Decimal(result) == Decimal('-10.0')


def test_generate_min_decimal_string_value_with_min_exclusive(generator: DecimalStringValueGenerator) -> None:
    restriction: Restriction = Restriction(
        name='test',
        base_type=BaseType(BaseType.decimal),
        total_digits=3,
        fraction_digits=0,
        min_exclusive=99.0
    )
    result: str = generator.generate_min_decimal_string_value(restriction)
    assert Decimal(result) == Decimal('100')


def test_generate_random_decimal_string_value_range(generator: DecimalStringValueGenerator) -> None:
    restriction: Restriction = Restriction(
        name='test',
        base_type=BaseType(BaseType.decimal),
        total_digits=4,
        fraction_digits=2,
        min_inclusive=-12.34,
        max_inclusive=45.67
    )
    for _ in range(10):
        value: str = generator.generate_random_decimal_string_value(restriction)
        assert Decimal('-12.34') <= Decimal(value) <= Decimal('45.67')
        digits: str = value.replace('.', '').lstrip('-').lstrip('0')
        assert len(digits) <= 4
        assert len(value.split('.')[-1]) <= 2
