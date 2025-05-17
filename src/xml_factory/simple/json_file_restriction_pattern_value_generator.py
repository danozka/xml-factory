import json
import logging
from logging import Logger
from pathlib import Path

from xml_factory import IRestrictionPatternValueGenerator, Restriction


class JsonFileRestrictionPatternValueGenerator(IRestrictionPatternValueGenerator):
    _log: Logger = logging.getLogger(__name__)
    _json_patterns_file_path: Path
    _pattern_values: dict[str, str]
    
    def __init__(self, json_patterns_file_path: Path) -> None:
        self._json_patterns_file_path = json_patterns_file_path
        self._log.info(f'Loading \'{self._json_patterns_file_path}\' patterns file...')
        if self._json_patterns_file_path.exists():
            with self._json_patterns_file_path.open('r') as file:
                self._pattern_values = json.load(file)
        else:
            self._log.info(f'Patterns file not found. Creating \'{self._json_patterns_file_path}\'...')
            self._pattern_values = {}
            self._json_patterns_file_path.parent.mkdir(parents=True, exist_ok=True)
            with self._json_patterns_file_path.open('w') as file:
                json.dump(obj=self._pattern_values, fp=file, indent=2)
            self._log.info(f'Patterns file \'{self._json_patterns_file_path}\' created')
        self._log.info(f'Patterns file \'{self._json_patterns_file_path}\' loaded')

    def generate_restriction_pattern_value(self, restriction: Restriction) -> str:
        if restriction.pattern in self._pattern_values:
            return self._pattern_values[restriction.pattern]
        else:
            prompt: str = (
                f'[{restriction.name}] Input {restriction.base_type} for the regular expression '
                f'\'{restriction.pattern}\''
            )
            if restriction.length is not None:
                prompt += f' + [length={restriction.min_length}]'
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
            self._pattern_values[restriction.pattern] = pattern_value
            return pattern_value

    def update_patterns(self) -> None:
        self._log.debug(f'Updating \'{self._json_patterns_file_path}\' patterns file...')
        with self._json_patterns_file_path.open('w') as file:
            json.dump(obj=self._pattern_values, fp=file, indent=2)
        self._log.info(f'Patterns file \'{self._json_patterns_file_path}\' updated')
