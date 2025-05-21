import json
import logging
from logging import Logger
from pathlib import Path

from pydantic import TypeAdapter

from json_patterns.domain.json_pattern import JsonPattern
from xml_factory import IRestrictionPatternValueGenerator, Restriction


class JsonFileRestrictionPatternValueGenerator(IRestrictionPatternValueGenerator):
    _INDENT_SPACES: int = 2
    _log: Logger = logging.getLogger(__name__)
    _json_patterns_file_path: Path
    _patterns: list[JsonPattern]
    
    def __init__(self, json_patterns_file_path: Path) -> None:
        self._json_patterns_file_path = json_patterns_file_path
        if self._json_patterns_file_path.exists():
            self._log.info(f'Loading \'{self._json_patterns_file_path}\' patterns file...')
            with self._json_patterns_file_path.open('r') as file:
                self._patterns = TypeAdapter(list[JsonPattern]).validate_json(file.read())
            self._log.info(f'Patterns file \'{self._json_patterns_file_path}\' loaded')
        else:
            self._log.info(f'Patterns file not found. Creating \'{self._json_patterns_file_path}\'...')
            self._patterns = []
            self._json_patterns_file_path.parent.mkdir(parents=True, exist_ok=True)
            self._save_patterns_to_file()
            self._log.info(f'Patterns file \'{self._json_patterns_file_path}\' created and loaded')

    def generate_restriction_pattern_value(self, element_name: str, restriction: Restriction) -> str:
        found_pattern: JsonPattern | None = self._find_pattern(restriction)
        if found_pattern is not None:
            return found_pattern.value
        else:
            prompt: str = (
                f'[{element_name}] Input \'{restriction.base_type.name}\' type for the regular expression '
                f'\'{restriction.pattern}\''
            )
            if restriction.length is not None:
                prompt += f' + [length={restriction.length}]'
            if restriction.min_length is not None:
                prompt += f' + [minLength={restriction.min_length}]'
            if restriction.max_length is not None:
                prompt += f' + [maxLength={restriction.max_length}]'
            if restriction.min_inclusive is not None:
                prompt += f' + [minInclusive={restriction.min_inclusive}]'
            if restriction.max_inclusive is not None:
                prompt += f' + [maxInclusive={restriction.max_inclusive}]'
            if restriction.min_exclusive is not None:
                prompt += f' + [minExclusive={restriction.min_exclusive}]'
            if restriction.max_exclusive is not None:
                prompt += f' + [maxExclusive={restriction.max_exclusive}]'
            if restriction.total_digits is not None:
                prompt += f' + [totalDigits={restriction.total_digits}]'
            if restriction.fraction_digits is not None:
                prompt += f' + [fractionDigits={restriction.fraction_digits}]'
            prompt += ': '
            pattern_value: str = input(prompt)
            self._patterns.append(
                JsonPattern(
                    pattern=restriction.pattern,
                    value=pattern_value,
                    length=restriction.length,
                    min_length=restriction.min_length,
                    max_length=restriction.max_length
                )
            )
            return pattern_value

    def update_patterns(self) -> None:
        self._log.debug(f'Updating \'{self._json_patterns_file_path}\' patterns file...')
        self._save_patterns_to_file()
        self._log.info(f'Patterns file \'{self._json_patterns_file_path}\' updated')
    
    def _save_patterns_to_file(self) -> None:
        with self._json_patterns_file_path.open('w') as file:
            json.dump(
                obj=TypeAdapter(list[JsonPattern]).dump_python(self._patterns, by_alias=True, exclude_none=True),
                fp=file,
                indent=self._INDENT_SPACES
            )
    
    def _find_pattern(self, restriction: Restriction) -> JsonPattern | None:
        pattern: JsonPattern
        for pattern in self._patterns:
            if (
                pattern.pattern == restriction.pattern and
                pattern.length == restriction.length and
                pattern.min_length == restriction.min_length and
                pattern.max_length == restriction.max_length
            ):
                return pattern
        return None
