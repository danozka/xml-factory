import pytest

from xml_factory.domain.base_type import BaseType
from xml_factory.domain.restriction import Restriction
from xml_factory.simple.any_uri_string_value_generator import AnyUriStringValueGenerator


@pytest.fixture
def generator() -> AnyUriStringValueGenerator:
    return AnyUriStringValueGenerator()


def test_specific_length_uri_is_correct(generator: AnyUriStringValueGenerator) -> None:
    length: int = 20
    uri: str = generator.generate_specific_length_any_uri_string_value(length)
    assert len(uri) == length
    assert uri.startswith(tuple(generator.SCHEMES))
    assert uri.endswith(generator.DOMAIN_EXTENSION)


def test_specific_length_uri_raises_error_for_insufficient_length(generator: AnyUriStringValueGenerator) -> None:
    with pytest.raises(ValueError):
        generator.generate_specific_length_any_uri_string_value(5)  # Too short for any valid URI


def test_random_uri_with_exact_length_restriction(generator: AnyUriStringValueGenerator) -> None:
    restriction: Restriction = Restriction(base_type=BaseType(BaseType.any_uri), length=15)
    uri: str = generator.generate_random_any_uri_string_value(restriction)
    assert len(uri) == 15
    assert uri.startswith(tuple(generator.SCHEMES))
    assert uri.endswith(generator.DOMAIN_EXTENSION)


def test_random_uri_with_min_length_restriction(generator: AnyUriStringValueGenerator) -> None:
    min_length: int = 20
    restriction: Restriction = Restriction(base_type=BaseType(BaseType.any_uri), min_length=min_length)
    uri: str = generator.generate_random_any_uri_string_value(restriction)
    assert len(uri) >= min_length
    assert uri.startswith(tuple(generator.SCHEMES))
    assert uri.endswith(generator.DOMAIN_EXTENSION)


def test_random_uri_with_max_length_restriction(generator: AnyUriStringValueGenerator) -> None:
    max_length: int = 25
    restriction: Restriction = Restriction(base_type=BaseType(BaseType.any_uri), max_length=max_length)
    uri: str = generator.generate_random_any_uri_string_value(restriction)
    assert len(uri) <= max_length
    assert uri.startswith(tuple(generator.SCHEMES))
    assert uri.endswith(generator.DOMAIN_EXTENSION)


def test_random_uri_with_min_and_max_length_restrictions(generator: AnyUriStringValueGenerator) -> None:
    min_length: int = 15
    max_length: int = 20
    restriction: Restriction = Restriction(
        base_type=BaseType(BaseType.any_uri),
        min_length=min_length,
        max_length=max_length
    )
    uri: str = generator.generate_random_any_uri_string_value(restriction)
    assert min_length <= len(uri) <= max_length
    assert uri.startswith(tuple(generator.SCHEMES))
    assert uri.endswith(generator.DOMAIN_EXTENSION)


def test_random_uri_handles_invalid_max_smaller_than_min(generator: AnyUriStringValueGenerator) -> None:
    min_length: int  = 20
    max_length: int  = 15
    restriction: Restriction = Restriction(
        base_type=BaseType(BaseType.any_uri),
        min_length=min_length,
        max_length=max_length
    )
    uri: str = generator.generate_random_any_uri_string_value(restriction)
    assert len(uri) == min_length
    assert uri.startswith(tuple(generator.SCHEMES))
    assert uri.endswith(generator.DOMAIN_EXTENSION)


def test_default_length_boundaries_when_not_specified(generator):
    restriction: Restriction = Restriction(base_type=BaseType(BaseType.any_uri))
    uri: str = generator.generate_random_any_uri_string_value(restriction)
    assert generator.RANDOM_MIN_LENGTH <= len(uri) <= generator.RANDOM_MAX_LENGTH
