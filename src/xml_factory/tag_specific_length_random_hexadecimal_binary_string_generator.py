import os


class TagSpecificLengthHexadecimalBinaryStringGenerator:
    @staticmethod
    def generate_specific_length_hexadecimal_binary_string_for_tag(length: int) -> str:
        return os.urandom(length).hex()
