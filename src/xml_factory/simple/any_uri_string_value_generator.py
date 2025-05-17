import random
from string import ascii_lowercase

from xml_factory.domain.restriction import Restriction


class AnyUriStringValueGenerator:
    SCHEMES: list[str] = ['http://', 'https://', 'ftp://']
    DOMAIN_EXTENSION: str = '.com'
    RANDOM_MIN_LENGTH: int = 20
    RANDOM_MAX_LENGTH: int = 30

    def generate_specific_length_any_uri_string_value(self, length: int) -> str:
        scheme: str = random.choice(self.SCHEMES)
        path_length: int = length - len(scheme) - len(self.DOMAIN_EXTENSION)
        if path_length <= 0:
            raise ValueError(f'Length of random anyURI is less than 0')
        return f"{scheme}{''.join(random.choices(population=ascii_lowercase, k=path_length))}{self.DOMAIN_EXTENSION}"

    def generate_random_any_uri_string_value(self, restriction: Restriction) -> str:
        if restriction.length is not None:
            return self.generate_specific_length_any_uri_string_value(restriction.length)
        min_length: int = restriction.min_length if restriction.min_length is not None else self.RANDOM_MIN_LENGTH
        max_length: int = restriction.max_length if restriction.max_length is not None else self.RANDOM_MAX_LENGTH
        if max_length < min_length:
            max_length = min_length
        random_length: int = random.randint(a=min_length, b=max_length)
        return self.generate_specific_length_any_uri_string_value(random_length)
