import random
from string import ascii_letters, digits

from xml_factory.domain.restriction import Restriction
from xml_factory.domain.white_space_restriction import WhiteSpaceRestriction


class StringValueGenerator:
    @staticmethod
    def generate_specific_length_string_value(
        length: int,
        white_space_restriction: WhiteSpaceRestriction | None = None
    ) -> str:
        result: str = ''.join(random.choices(population=(ascii_letters + digits), k=length))
        if white_space_restriction == WhiteSpaceRestriction.replace:
            result = result.replace(' ', '_')
        elif white_space_restriction == WhiteSpaceRestriction.collapse:
            result = ' '.join(result.split())
        return result

    @staticmethod
    def generate_random_string_value(restriction: Restriction) -> str:
        result: str
        min_length: int | None = restriction.min_length
        max_length: int | None = restriction.max_length
        if restriction.pattern is not None:
            input_string: str = (
                f'[{restriction.name}] Input string for the regular expression \'{restriction.pattern}\'')
            if min_length is not None:
                input_string += f' + [minLength={min_length}]'
            if max_length is not None:
                input_string += f' + [maxLength={max_length}]'
            input_string += ': '
            result = input(input_string)
        else:
            if min_length is None:
                min_length = 1
            if max_length is None:
                max_length = 10
            length: int = random.randint(a=min_length, b=max_length)
            result = ''.join(random.choices(population=(ascii_letters + digits), k=length))
        if restriction.white_space == WhiteSpaceRestriction.replace:
            result = result.replace(' ', '_')
        elif restriction.white_space == WhiteSpaceRestriction.collapse:
            result = ' '.join(result.split())
        return result
