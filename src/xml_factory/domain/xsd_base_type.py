from enum import StrEnum


class XsdBaseType(StrEnum):
    date_time = 'dateTime'
    time = 'time'
    date = 'date'
    boolean = 'boolean'
    hex_binary = 'hexBinary'
    string = 'string'
    decimal = 'decimal'
    integer = 'integer'
