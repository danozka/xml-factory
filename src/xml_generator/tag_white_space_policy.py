from enum import StrEnum


class TagWhiteSpacePolicy(StrEnum):
    collapse = 'collapse'
    preserve = 'preserve'
    replace = 'replace'
