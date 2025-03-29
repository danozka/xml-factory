from dataclasses import dataclass
from typing import Dict, Optional, Union

from xml_factory.domain.xsd_all import XsdAll
from xml_factory.domain.xsd_attribute import XsdAttribute
from xml_factory.domain.xsd_choice import XsdChoice
from xml_factory.domain.xsd_component import XsdComponent
from xml_factory.domain.xsd_sequence import XsdSequence


@dataclass
class XsdComplexType(XsdComponent):
    """Element that can contain attributes and child elements"""
    abstract: bool = False
    mixed: bool = False  # mixed content (text + elements)
    content_model: Optional[Union[XsdSequence, XsdChoice, XsdAll]] = None
    attributes: Dict[str, XsdAttribute] = None
    base_type: Optional[Union[str, 'XsdComplexType']] = None
    derived_by: Optional[str] = None  # 'extension' or 'restriction'
