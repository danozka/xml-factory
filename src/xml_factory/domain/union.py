from dataclasses import dataclass

from xml_factory.domain.simple_type import SimpleType


@dataclass
class Union(SimpleType):
    member_types: list[SimpleType] | None = None
