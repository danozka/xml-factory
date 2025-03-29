from dataclasses import dataclass
from typing import Optional, Union

from xml_factory.domain.xsd_all import XsdAll
from xml_factory.domain.xsd_choice import XsdChoice
from xml_factory.domain.xsd_component import XsdComponent
from xml_factory.domain.xsd_sequence import XsdSequence


@dataclass
class XsdGroup(XsdComponent):
    """Reusable group of elements"""
    content_model: Optional[Union[XsdSequence, XsdChoice, XsdAll]] = None
