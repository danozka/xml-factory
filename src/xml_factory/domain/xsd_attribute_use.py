from enum import StrEnum


class XsdAttributeUse(StrEnum):
    optional = 'optional'
    prohibited = 'prohibited'
    required = 'required'
