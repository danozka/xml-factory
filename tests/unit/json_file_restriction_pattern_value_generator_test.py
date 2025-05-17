import json
from pathlib import Path
from typing import Generator
from unittest.mock import MagicMock, patch

import pytest

from xml_factory.domain.base_type import BaseType
from xml_factory.domain.restriction import Restriction
from xml_factory.simple.json_file_restriction_pattern_value_generator import JsonFileRestrictionPatternValueGenerator


@pytest.fixture
def temp_json_file(tmp_path: Path) -> Generator[Path, None, None]:
    temp_json_file: Path = tmp_path / 'patterns.json'
    yield temp_json_file
    if temp_json_file.exists():
        temp_json_file.unlink()


@pytest.fixture
def generator_without_patterns(temp_json_file: Path) -> JsonFileRestrictionPatternValueGenerator:
    return JsonFileRestrictionPatternValueGenerator(temp_json_file)


@pytest.fixture
def generator_with_patterns(temp_json_file: Path) -> JsonFileRestrictionPatternValueGenerator:
    patterns: dict[str, str] = {
        '[a-z]+': 'abc',
        '\\d{3}-\\d{2}-\\d{4}': '123-45-6789'
    }
    temp_json_file.parent.mkdir(parents=True, exist_ok=True)
    temp_json_file.write_text(json.dumps(patterns))
    return JsonFileRestrictionPatternValueGenerator(temp_json_file)


def test_init_creates_file_if_not_exists(temp_json_file: Path) -> None:
    assert not temp_json_file.exists()
    JsonFileRestrictionPatternValueGenerator(temp_json_file)
    assert temp_json_file.exists()
    with open(file=temp_json_file, mode='r') as f:
        content: dict[str, str] = json.load(f)
    assert content == {}


def test_generate_restriction_pattern_value_existing_pattern(
    generator_with_patterns: JsonFileRestrictionPatternValueGenerator
) -> None:
    restriction: Restriction = Restriction(
        name='test',
        base_type=BaseType(BaseType.string),
        pattern='[a-z]+'
    )
    result: str = generator_with_patterns.generate_restriction_pattern_value(restriction)
    assert result == 'abc'


def test_generate_restriction_pattern_value_new_pattern(
    generator_without_patterns: JsonFileRestrictionPatternValueGenerator
) -> None:
    restriction: Restriction = Restriction(
        name='test',
        base_type=BaseType(BaseType.string),
        pattern='[a-z0-9]+'
    )
    mock_return_value: str = 'test123'
    mock_input: MagicMock
    with patch(target='builtins.input', return_value=mock_return_value) as mock_input:
        result: str = generator_without_patterns.generate_restriction_pattern_value(restriction)
    assert result == mock_return_value
    mock_input.assert_called_once()


def test_update_patterns(
    generator_with_patterns: JsonFileRestrictionPatternValueGenerator,
    temp_json_file: Path
) -> None:
    pattern: str = '^[A-Z][a-z]*$'
    restriction: Restriction = Restriction(
        name='test',
        base_type=BaseType(BaseType.string),
        pattern=pattern
    )
    mock_return_value: str = 'Hello'
    mock_input: MagicMock
    with patch(target='builtins.input', return_value=mock_return_value) as mock_input:
        result: str = generator_with_patterns.generate_restriction_pattern_value(restriction)
    assert result == mock_return_value
    mock_input.assert_called_once()
    generator_with_patterns.update_patterns()
    with open(file=temp_json_file, mode='r') as f:
        updated_patterns: dict[str, str] = json.load(f)
    assert pattern in updated_patterns
    assert updated_patterns[pattern] == mock_return_value
