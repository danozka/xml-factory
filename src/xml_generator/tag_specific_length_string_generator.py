import random
from string import ascii_letters, digits

from xml_generator.tag_white_space_policy import TagWhiteSpacePolicy


class TagSpecificLengthStringGenerator:
    @staticmethod
    def generate_specific_length_string_for_tag(
        length: int,
        white_space_policy: TagWhiteSpacePolicy | None = None
    ) -> str:
        result: str = ''.join(random.choices(population=(ascii_letters + digits), k=length))
        if white_space_policy == TagWhiteSpacePolicy.replace:
            result = result.replace(' ', '_')
        elif white_space_policy == TagWhiteSpacePolicy.collapse:
            result = ' '.join(result.split())
        return result
