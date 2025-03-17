import os
import random


class TagRandomHexadecimalBinaryStringGenerator:
    @staticmethod
    def generate_random_hexadecimal_binary_string_for_tag(
        min_length: int | None = None,
        max_length: int | None = None
    ) -> str:
        result: str
        if min_length is None:
            min_length = 1
        if max_length is None:
            max_length = 10
        length: int = random.randint(a=min_length, b=max_length) // 2
        result: str = os.urandom(length).hex()
        return result
