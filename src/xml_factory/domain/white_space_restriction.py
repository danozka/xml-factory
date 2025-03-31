from enum import StrEnum


class XsdWhiteSpaceRestriction(StrEnum):
    collapse = 'collapse'
    preserve = 'preserve'
    replace = 'replace'
