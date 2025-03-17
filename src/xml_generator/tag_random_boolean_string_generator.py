import random


class TagRandomBooleanStringGenerator:
    @staticmethod
    def generate_random_boolean_string_for_tag() -> str:
        return str(bool(random.randint(a=0, b=1))).lower()
