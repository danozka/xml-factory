from xml_factory.domain.base_type import BaseType
from xml_factory.domain.restriction import Restriction
from xml_factory.simple.base_restriction_value_generator import BaseRestrictionValueGenerator
from xml_factory.simple.i_restriction_value_generator import IRestrictionValueGenerator


class RestrictionMaxValueGenerator(BaseRestrictionValueGenerator, IRestrictionValueGenerator):
    def generate_restriction_value(self, restriction: Restriction) -> str:
        if restriction.base_type == BaseType.any_uri:
            if restriction.max_length is not None:
                return self._any_uri_string_value_generator.generate_specific_length_any_uri_string_value(
                    restriction.max_length
                )
            else:
                return self._any_uri_string_value_generator.generate_random_any_uri_string_value(restriction)
        elif restriction.base_type == BaseType.base_64_binary:
            if restriction.max_length is not None:
                return self._binary_string_value_generator.generate_specific_size_base64_binary_string_value(
                    restriction.max_length
                )
            else:
                return self._binary_string_value_generator.generate_random_base64_binary_string_value(restriction)
        elif restriction.base_type == BaseType.boolean:
            return self._boolean_string_value_generator.generate_random_boolean_string_value()
        elif restriction.base_type == BaseType.date:
            return self._date_string_value_generator.generate_max_date_string_value(restriction)
        elif restriction.base_type == BaseType.date_time:
            return self._date_time_string_value_generator.generate_max_date_time_string_value(restriction)
        elif restriction.base_type == BaseType.decimal or restriction.base_type == BaseType.float:
            return self._decimal_string_value_generator.generate_max_decimal_string_value(restriction)
        elif restriction.base_type == BaseType.gregorian_day:
            return self._gregorian_day_string_value_generator.generate_max_gregorian_day_string_value(restriction)
        elif restriction.base_type == BaseType.gregorian_month:
            return self._gregorian_month_string_value_generator.generate_random_gregorian_month_string_value(
                restriction
            )
        elif restriction.base_type == BaseType.gregorian_month_day:
            return self._gregorian_month_day_string_value_generator.generate_max_gregorian_month_day_string_value(
                restriction
            )
        elif restriction.base_type == BaseType.gregorian_year:
            return self._gregorian_year_string_value_generator.generate_max_gregorian_year_string_value(restriction)
        elif restriction.base_type == BaseType.gregorian_year_month:
            return self._gregorian_year_month_string_value_generator.generate_max_gregorian_year_month_string_value(
                restriction
            )
        elif restriction.base_type == BaseType.hex_binary:
            if restriction.max_length is not None:
                return self._binary_string_value_generator.generate_specific_size_hex_binary_string_value(
                    restriction.max_length
                )
            else:
                return self._binary_string_value_generator.generate_random_hex_binary_string_value(restriction)
        elif restriction.base_type == BaseType.integer:
            return self._integer_string_value_generator.generate_max_integer_string_value(restriction)
        elif restriction.base_type == BaseType.string:
            if restriction.max_length is not None:
                return self._string_value_generator.generate_specific_length_string_value(restriction.max_length)
            else:
                return self._string_value_generator.generate_random_string_value(restriction)
        elif restriction.base_type == BaseType.time:
            return self._time_string_value_generator.generate_max_time_string_value(restriction)
        else:
            raise NotImplementedError(f'Unsupported restriction base type \'{restriction.base_type}\'')
