from decimal import Decimal
from enum import Enum

from elementpath.datatypes import (
    AnyURI,
    Base64Binary,
    Date10,
    DateTime10,
    GregorianDay,
    GregorianMonth,
    GregorianMonthDay,
    GregorianYear10,
    GregorianYearMonth10,
    HexBinary,
    Time
)


class BaseType(Enum):
    any_uri = AnyURI
    base_64_binary = Base64Binary
    boolean = bool
    date = Date10
    date_time = DateTime10
    decimal = Decimal
    float = float
    gregorian_day = GregorianDay
    gregorian_month = GregorianMonth
    gregorian_month_day = GregorianMonthDay
    gregorian_year = GregorianYear10
    gregorian_year_month = GregorianYearMonth10
    hex_binary = HexBinary
    integer = int
    string = str
    time = Time
