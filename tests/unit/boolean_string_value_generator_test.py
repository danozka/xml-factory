import pytest

from xml_factory.simple.boolean_string_value_generator import BooleanStringValueGenerator


@pytest.fixture
def generator() -> BooleanStringValueGenerator:
    return BooleanStringValueGenerator()


def test_generate_random_boolean_string_value(generator: BooleanStringValueGenerator) -> None:
    result: str = generator.generate_random_boolean_string_value()
    assert result in ['true', 'false']


def test_multiple_calls_can_return_different_values(generator: BooleanStringValueGenerator) -> None:
    results: set[str] = set()
    for _ in range(1000):
        results.add(generator.generate_random_boolean_string_value())
        if len(results) == 2:
            break
    assert len(results) == 2
    assert 'true' in results
    assert 'false' in results
