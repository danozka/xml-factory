from dataclasses import dataclass

from xml_factory.domain.xsd_content_model import XsdContentModel


@dataclass
class XsdChoice(XsdContentModel):
    """Only one of these elements may appear"""
    min_occurs: int = 1
    max_occurs: int = 1
