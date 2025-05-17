from xml_factory.simple.any_uri_string_value_generator import AnyUriStringValueGenerator
from xml_factory.simple.binary_string_value_generator import BinaryStringValueGenerator
from xml_factory.simple.boolean_string_value_generator import BooleanStringValueGenerator
from xml_factory.simple.date_string_value_generator import DateStringValueGenerator
from xml_factory.simple.date_time_string_value_generator import DateTimeStringValueGenerator
from xml_factory.simple.decimal_string_value_generator import DecimalStringValueGenerator
from xml_factory.simple.gregorian_day_string_value_generator import GregorianDayStringValueGenerator
from xml_factory.simple.gregorian_month_day_string_value_generator import GregorianMonthDayStringValueGenerator
from xml_factory.simple.gregorian_month_string_value_generator import GregorianMonthStringValueGenerator
from xml_factory.simple.gregorian_year_month_value_generator import GregorianYearMonthStringValueGenerator
from xml_factory.simple.gregorian_year_string_value_generator import GregorianYearStringValueGenerator
from xml_factory.simple.integer_string_value_generator import IntegerStringValueGenerator
from xml_factory.simple.string_value_generator import StringValueGenerator
from xml_factory.simple.time_string_value_generator import TimeStringValueGenerator


class BaseRestrictionValueGenerator:
    _any_uri_string_value_generator: AnyUriStringValueGenerator
    _binary_string_value_generator: BinaryStringValueGenerator
    _boolean_string_value_generator: BooleanStringValueGenerator
    _date_string_value_generator: DateStringValueGenerator
    _date_time_string_value_generator: DateTimeStringValueGenerator
    _decimal_string_value_generator: DecimalStringValueGenerator
    _gregorian_day_string_value_generator: GregorianDayStringValueGenerator
    _gregorian_month_day_string_value_generator: GregorianMonthDayStringValueGenerator
    _gregorian_month_string_value_generator: GregorianMonthStringValueGenerator
    _gregorian_year_month_string_value_generator: GregorianYearMonthStringValueGenerator
    _gregorian_year_string_value_generator: GregorianYearStringValueGenerator
    _integer_string_value_generator: IntegerStringValueGenerator
    _string_value_generator: StringValueGenerator
    _time_string_value_generator: TimeStringValueGenerator
    
    def __init__(
        self,
        any_uri_string_value_generator: AnyUriStringValueGenerator = AnyUriStringValueGenerator(),
        binary_string_value_generator: BinaryStringValueGenerator = BinaryStringValueGenerator(),
        boolean_string_value_generator: BooleanStringValueGenerator = BooleanStringValueGenerator(),
        date_string_value_generator: DateStringValueGenerator = DateStringValueGenerator(),
        date_time_string_value_generator: DateTimeStringValueGenerator = DateTimeStringValueGenerator(),
        decimal_string_value_generator: DecimalStringValueGenerator = DecimalStringValueGenerator(),
        gregorian_day_string_value_generator: GregorianDayStringValueGenerator = GregorianDayStringValueGenerator(),
        gregorian_month_day_string_value_generator: GregorianMonthDayStringValueGenerator = (
                GregorianMonthDayStringValueGenerator()
        ),
        gregorian_month_string_value_generator: GregorianMonthStringValueGenerator = (
                GregorianMonthStringValueGenerator()
        ),
        gregorian_year_month_string_value_generator: GregorianYearMonthStringValueGenerator = (
                GregorianYearMonthStringValueGenerator()
        ),
        gregorian_year_string_value_generator: GregorianYearStringValueGenerator = GregorianYearStringValueGenerator(),
        integer_string_value_generator: IntegerStringValueGenerator = IntegerStringValueGenerator(),
        string_value_generator: StringValueGenerator = StringValueGenerator(),
        time_string_value_generator: TimeStringValueGenerator = TimeStringValueGenerator()
    ) -> None:
        self._any_uri_string_value_generator = any_uri_string_value_generator
        self._binary_string_value_generator = binary_string_value_generator
        self._boolean_string_value_generator = boolean_string_value_generator
        self._date_string_value_generator = date_string_value_generator
        self._date_time_string_value_generator = date_time_string_value_generator
        self._decimal_string_value_generator = decimal_string_value_generator
        self._gregorian_day_string_value_generator = gregorian_day_string_value_generator
        self._gregorian_month_day_string_value_generator = gregorian_month_day_string_value_generator
        self._gregorian_month_string_value_generator = gregorian_month_string_value_generator
        self._gregorian_year_month_string_value_generator = gregorian_year_month_string_value_generator
        self._gregorian_year_string_value_generator = gregorian_year_string_value_generator
        self._integer_string_value_generator = integer_string_value_generator
        self._string_value_generator = string_value_generator
        self._time_string_value_generator = time_string_value_generator
