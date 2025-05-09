import json
import logging
from logging import Logger
from pathlib import Path

from xml_factory import BaseType, IRestrictionPatternValueGenerator, Restriction


class JsonFileRestrictionPatternValueGenerator(IRestrictionPatternValueGenerator):
    _log: Logger = logging.getLogger(__name__)
    _json_patterns_file_path: Path
    _pattern_values: dict[str, str]
    
    def __init__(self, json_patterns_file_path: Path) -> None:
        self._json_patterns_file_path = json_patterns_file_path
        if self._json_patterns_file_path.exists():
            self._log.debug(f'Loading \'{self._json_patterns_file_path}\' patterns file...')
            with self._json_patterns_file_path.open('r') as file:
                self._pattern_values = json.load(file)
        else:
            self._log.warning(f'Patterns file not found. Creating \'{self._json_patterns_file_path}\'...')
            self._pattern_values = {}
            self._json_patterns_file_path.parent.mkdir(parents=True, exist_ok=True)
            with self._json_patterns_file_path.open('w') as file:
                json.dump(obj=self._pattern_values, fp=file, indent=2)

    def generate_restriction_pattern_value(self, restriction: Restriction) -> str:
        if restriction.pattern in self._pattern_values:
            return self._pattern_values[restriction.pattern]
        else:
            pattern_value: str
            if restriction.base_type == BaseType.string:
                min_length: int | None = restriction.min_length
                max_length: int | None = restriction.max_length
                input_string: str = (
                    f'[{restriction.name}] Input string for the regular expression \'{restriction.pattern}\'')
                if min_length is not None:
                    input_string += f' + [minLength={min_length}]'
                if max_length is not None:
                    input_string += f' + [maxLength={max_length}]'
                input_string += ': '
                pattern_value = input(input_string)
            else:
                pattern_value = input(
                    f'[{restriction.name}] Input {restriction.base_type} for the regular expression '
                    f'\'{restriction.pattern}\': '
                )
            self._pattern_values[restriction.pattern] = pattern_value
            return pattern_value

    def update_patterns(self) -> None:
        self._log.debug(f'Updating \'{self._json_patterns_file_path}\' patterns file...')
        with self._json_patterns_file_path.open('w') as file:
            json.dump(obj=self._pattern_values, fp=file, indent=2)
        self._log.debug(f'Patterns file \'{self._json_patterns_file_path}\' updated')
