from enum import StrEnum


class WhiteSpaceRestriction(StrEnum):
    collapse = 'collapse'
    preserve = 'preserve'
    replace = 'replace'
