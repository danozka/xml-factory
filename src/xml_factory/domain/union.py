from dataclasses import dataclass
from typing import List, Optional

from xml_factory.domain.xsd_simple_type import XsdSimpleType


@dataclass
class XsdUnion(XsdSimpleType):
    member_types: Optional[List[XsdSimpleType]] = None
