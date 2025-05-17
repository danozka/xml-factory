import base64
import os
import random

from xml_factory.domain.restriction import Restriction


class BinaryStringValueGenerator:
    RANDOM_MIN_SIZE: int = 8
    RANDOM_MAX_SIZE: int = 32

    @staticmethod
    def generate_specific_size_hex_binary_string_value(size: int) -> str:
        return os.urandom(size).hex()

    def generate_random_hex_binary_string_value(self, restriction: Restriction) -> str:
        if restriction.length is not None:
            return self.generate_specific_size_hex_binary_string_value(restriction.length)
        return self.generate_specific_size_hex_binary_string_value(self._get_size(restriction))

    @staticmethod
    def generate_specific_size_base64_binary_string_value(size: int) -> str:
        return base64.b64encode(os.urandom(size)).decode('ascii')

    def generate_random_base64_binary_string_value(self, restriction: Restriction) -> str:
        if restriction.length is not None:
            return self.generate_specific_size_base64_binary_string_value(restriction.length)
        return self.generate_specific_size_base64_binary_string_value(self._get_size(restriction))

    def _get_size(self, restriction: Restriction) -> int:
        min_size: int = restriction.min_length if restriction.min_length is not None else self.RANDOM_MIN_SIZE
        max_size: int = restriction.max_length if restriction.max_length is not None else self.RANDOM_MAX_SIZE
        if max_size < min_size:
            max_size = min_size
        return random.randint(a=min_size, b=max_size)
