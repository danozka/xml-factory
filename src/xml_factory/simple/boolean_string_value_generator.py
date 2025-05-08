import random


class BooleanStringValueGenerator:
    @staticmethod
    def generate_random_boolean_string_value() -> str:
        return str(bool(random.randint(a=0, b=1))).lower()
