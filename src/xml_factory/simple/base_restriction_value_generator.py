from xml_factory.simple.boolean_string_value_generator import BooleanStringValueGenerator
from xml_factory.simple.date_string_value_generator import DateStringValueGenerator
from xml_factory.simple.date_time_string_value_generator import DateTimeStringValueGenerator
from xml_factory.simple.decimal_string_value_generator import DecimalStringValueGenerator
from xml_factory.simple.hexadecimal_binary_string_value_generator import HexadecimalBinaryStringValueGenerator
from xml_factory.simple.integer_string_value_generator import IntegerStringValueGenerator
from xml_factory.simple.string_value_generator import StringValueGenerator
from xml_factory.simple.time_string_value_generator import TimeStringValueGenerator


class BaseRestrictionValueGenerator:
    _boolean_string_value_generator: BooleanStringValueGenerator
    _date_string_value_generator: DateStringValueGenerator
    _date_time_string_value_generator: DateTimeStringValueGenerator
    _decimal_string_value_generator: DecimalStringValueGenerator
    _hexadecimal_binary_string_value_generator: HexadecimalBinaryStringValueGenerator
    _integer_string_value_generator: IntegerStringValueGenerator
    _string_value_generator: StringValueGenerator
    _time_string_value_generator: TimeStringValueGenerator
    
    def __init__(
        self,
        boolean_string_value_generator: BooleanStringValueGenerator = BooleanStringValueGenerator(),
        date_string_value_generator: DateStringValueGenerator = DateStringValueGenerator(),
        date_time_string_value_generator: DateTimeStringValueGenerator = DateTimeStringValueGenerator(),
        decimal_string_value_generator: DecimalStringValueGenerator = DecimalStringValueGenerator(),
        hexadecimal_binary_string_value_generator: HexadecimalBinaryStringValueGenerator = (
            HexadecimalBinaryStringValueGenerator()
        ),
        integer_string_value_generator: IntegerStringValueGenerator = IntegerStringValueGenerator(),
        string_value_generator: StringValueGenerator = StringValueGenerator(),
        time_string_value_generator: TimeStringValueGenerator = TimeStringValueGenerator()
    ) -> None:
        self._boolean_string_value_generator = boolean_string_value_generator
        self._date_string_value_generator = date_string_value_generator
        self._date_time_string_value_generator = date_time_string_value_generator
        self._decimal_string_value_generator = decimal_string_value_generator
        self._hexadecimal_binary_string_value_generator = hexadecimal_binary_string_value_generator
        self._integer_string_value_generator = integer_string_value_generator
        self._string_value_generator = string_value_generator
        self._time_string_value_generator = time_string_value_generator
