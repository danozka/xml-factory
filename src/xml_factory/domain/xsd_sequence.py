from dataclasses import dataclass
from typing import Union

from xml_factory.domain.xsd_content_model import XsdContentModel


@dataclass
class XsdSequence(XsdContentModel):
    """Elements must appear in this order"""
    min_occurs: int = 1
    max_occurs: Union[int, str] = 1
