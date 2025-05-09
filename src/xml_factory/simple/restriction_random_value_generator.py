import random

from xml_factory.domain.base_type import BaseType
from xml_factory.domain.restriction import Restriction
from xml_factory.simple.base_restriction_value_generator import BaseRestrictionValueGenerator
from xml_factory.simple.i_restriction_value_generator import IRestrictionValueGenerator


class RestrictionRandomValueGenerator(BaseRestrictionValueGenerator, IRestrictionValueGenerator):
    def generate_restriction_value(self, restriction: Restriction) -> str:
        if restriction.enumeration is not None:
            return random.choice(restriction.enumeration)
        elif restriction.base_type == BaseType.time:
            return self._time_string_value_generator.generate_random_time_string_value()
        elif restriction.base_type == BaseType.boolean:
            return self._boolean_string_value_generator.generate_random_boolean_string_value()
        elif restriction.base_type == BaseType.date_time:
            return self._date_time_string_value_generator.generate_random_date_time_string_value()
        elif restriction.base_type == BaseType.date:
            return self._date_string_value_generator.generate_random_date_string_value()
        elif restriction.base_type == BaseType.string:
            return self._string_value_generator.generate_random_string_value(restriction)
        elif restriction.base_type == BaseType.integer:
            return self._integer_string_value_generator.generate_random_integer_string_value(restriction)
        elif restriction.base_type == BaseType.decimal:
            return self._decimal_string_value_generator.generate_random_decimal_string_value(restriction)
        elif restriction.base_type == BaseType.hex_binary:
            return self._hexadecimal_binary_string_value_generator.generate_random_hexadecimal_binary_string_value(
                restriction
            )
        else:
            raise NotImplementedError(f'Unsupported restriction base type \'{restriction.base_type}\'')
