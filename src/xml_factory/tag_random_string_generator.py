import random
from string import ascii_letters, digits

from xml_factory.tag_white_space_policy import TagWhiteSpacePolicy


class TagRandomStringGenerator:
    @staticmethod
    def generate_random_string_for_tag(
        tag_name: str = 'TAG',
        min_length: int | None = None,
        max_length: int | None = None,
        pattern: str | None = None,
        white_space_policy: TagWhiteSpacePolicy | None = None,
        force_min_length: bool = False,
        force_max_length: bool = False
    ) -> str:
        result: str
        if pattern is not None:
            input_string: str = f'[{tag_name}] Input string for the regular expression \'{pattern}\''
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
        if white_space_policy == TagWhiteSpacePolicy.replace:
            result = result.replace(' ', '_')
        elif white_space_policy == TagWhiteSpacePolicy.collapse:
            result = ' '.join(result.split())
        return result
