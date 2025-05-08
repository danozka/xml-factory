import os
import random

from xml_factory.domain.restriction import Restriction


class HexadecimalBinaryStringValueGenerator:
    @staticmethod
    def generate_random_hexadecimal_binary_string_value(restriction: Restriction) -> str:
        min_length: int | None = restriction.min_length
        max_length: int | None = restriction.max_length
        result: str
        if min_length is None:
            min_length = 1
        if max_length is None:
            max_length = 10
        length: int = random.randint(a=min_length, b=max_length) // 2
        result: str = os.urandom(length).hex()
        return result

    @staticmethod
    def generate_specific_length_hexadecimal_binary_string_value(length: int) -> str:
        return os.urandom(length).hex()
