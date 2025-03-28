class TagDecimalStringGenerator:
    @staticmethod
    def generate_decimal_string_for_tag(value: float, fraction_digits: int | None = None) -> str:
        if fraction_digits is None:
            fraction_digits = 2
        return f'{value:.{fraction_digits}f}'
