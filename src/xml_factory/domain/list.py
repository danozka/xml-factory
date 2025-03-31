from dataclasses import dataclass
from typing import Optional

from xml_factory.domain.xsd_simple_type import XsdSimpleType


@dataclass
class XsdList(XsdSimpleType):
    item_type: Optional[XsdSimpleType] = None
