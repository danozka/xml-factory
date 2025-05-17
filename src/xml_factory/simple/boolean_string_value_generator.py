import random


class BooleanStringValueGenerator:
    @staticmethod
    def generate_random_boolean_string_value() -> str:
        return str(random.choice([True, False])).lower()
