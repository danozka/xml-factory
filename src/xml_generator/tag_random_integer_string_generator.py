import random


class TagRandomIntegerStringGenerator:
    @staticmethod
    def generate_random_integer_string_for_tag(
        tag_name: str = 'TAG',
        pattern: str | None = None,
        min_inclusive: int | None = None,
        max_inclusive: int | None = None,
        min_exclusive: int | None = None,
        max_exclusive: int | None = None,
        total_digits: int | None = None
    ) -> str:
        if pattern is not None:
            return input(f'[{tag_name}] Input integer for the regular expression \'{pattern}\': ')
        if min_inclusive is None:
            min_inclusive = 0
        if max_inclusive is None:
            max_inclusive = 10
        if min_exclusive is not None and min_exclusive > min_inclusive:
            min_inclusive = min_exclusive + 1
        if max_exclusive is not None and max_exclusive < max_inclusive:
            max_inclusive = max_exclusive - 1
        if total_digits is not None:
            min_inclusive = max(min_inclusive, 10 ** (total_digits - 1))
            max_inclusive = min(max_inclusive, (10 ** total_digits) - 1)
        return str(random.randint(a=min_inclusive, b=max_inclusive))
