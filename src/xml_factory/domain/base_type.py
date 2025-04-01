from enum import StrEnum


class BaseType(StrEnum):
    date_time = 'dateTime'
    time = 'time'
    date = 'date'
    boolean = 'boolean'
    hex_binary = 'hexBinary'
    string = 'string'
    decimal = 'decimal'
    integer = 'integer'
