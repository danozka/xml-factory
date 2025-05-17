import re
import base64

import pytest

from xml_factory import BaseType
from xml_factory.domain.restriction import Restriction
from xml_factory.simple.binary_string_value_generator import BinaryStringValueGenerator


@pytest.fixture
def generator() -> BinaryStringValueGenerator:
    return BinaryStringValueGenerator()


def test_generate_specific_size_hex_binary_string_value(generator: BinaryStringValueGenerator) -> None:
    size: int
    for size in [4, 8, 16]:
        result: str = generator.generate_specific_size_hex_binary_string_value(size)
        assert len(result) == size * 2
        assert all(c in '0123456789abcdef' for c in result.lower())


def test_generate_random_hex_binary_string_value_with_length(generator: BinaryStringValueGenerator) -> None:
    restriction: Restriction = Restriction(name='test', base_type=BaseType(BaseType.hex_binary), length=10)
    result: str = generator.generate_random_hex_binary_string_value(restriction)
    assert len(result) == restriction.length * 2
    assert all(c in '0123456789abcdef' for c in result.lower())


def test_generate_random_hex_binary_string_value_with_min_max_length(generator: BinaryStringValueGenerator) -> None:
    min_length: int = 5
    max_length: int = 10
    restriction: Restriction = Restriction(
        name='test',
        base_type=BaseType(BaseType.hex_binary),
        min_length=min_length,
        max_length=max_length
    )
    result: str = generator.generate_random_hex_binary_string_value(restriction)
    actual_bytes_size: int = len(result) // 2
    assert min_length <= actual_bytes_size <= max_length
    assert all(c in '0123456789abcdef' for c in result.lower())


def test_generate_specific_size_base64_binary_string_value(generator: BinaryStringValueGenerator) -> None:
    size: int
    for size in [3, 6, 9]:
        result: str = generator.generate_specific_size_base64_binary_string_value(size)
        pattern: str = r'^[A-Za-z0-9+/]+={0,2}$'
        assert re.match(pattern, result)
        decoded: bytes = base64.b64decode(result)
        assert len(decoded) == size


def test_generate_random_base64_binary_string_value_with_length(generator: BinaryStringValueGenerator) -> None:
    restriction: Restriction = Restriction(name='test', base_type=BaseType(BaseType.hex_binary), length=12)
    result: str = generator.generate_random_base64_binary_string_value(restriction)
    pattern: str = r'^[A-Za-z0-9+/]+={0,2}$'
    assert re.match(pattern, result)
    decoded: bytes = base64.b64decode(result)
    assert len(decoded) == restriction.length


def test_generate_random_base64_binary_string_value_with_min_max_length(generator: BinaryStringValueGenerator) -> None:
    min_length: int = 5
    max_length: int = 10
    restriction: Restriction = Restriction(
        name='test',
        base_type=BaseType(BaseType.hex_binary),
        min_length=min_length,
        max_length=max_length
    )
    result: str = generator.generate_random_base64_binary_string_value(restriction)
    pattern: str = r'^[A-Za-z0-9+/]+={0,2}$'
    assert re.match(pattern, result)
    decoded: bytes = base64.b64decode(result)
    assert min_length <= len(decoded) <= max_length
