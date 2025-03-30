from dataclasses import dataclass
from typing import Optional


@dataclass
class XsdComponent:
    """Base class for all XSD components"""
    name: Optional[str] = None
