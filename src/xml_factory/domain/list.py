from dataclasses import dataclass

from xml_factory.domain.simple_type import SimpleType


@dataclass
class List(SimpleType):
    item_type: SimpleType | None = None
