import random
from string import ascii_letters

from xml_factory.domain.restriction import Restriction


class StringValueGenerator:
    RANDOM_MIN_LENGTH: int = 10
    RANDOM_MAX_LENGTH: int = 30

    @staticmethod
    def generate_specific_length_string_value(length: int) -> str:
        return ''.join(random.choices(population=ascii_letters, k=length))

    def generate_random_string_value(self, restriction: Restriction) -> str:
        if restriction.length is not None:
            return self.generate_specific_length_string_value(restriction.length)
        min_length: int = restriction.min_length if restriction.min_length is not None else self.RANDOM_MIN_LENGTH
        max_length: int = restriction.max_length if restriction.max_length is not None else self.RANDOM_MAX_LENGTH
        if max_length < min_length:
            max_length = min_length
        random_length: int = random.randint(a=min_length, b=max_length)
        return self.generate_specific_length_string_value(random_length)
