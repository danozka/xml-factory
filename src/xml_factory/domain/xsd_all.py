from dataclasses import dataclass

from xml_factory.domain.xsd_content_model import XsdContentModel


@dataclass
class XsdAll(XsdContentModel):
    """Elements may appear in any order"""
    pass
