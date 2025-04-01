from dataclasses import dataclass, field
from typing import Optional

from xml_factory.domain.attribute_group import AttributeGroup
from xml_factory.domain.complex_type import ComplexType
from xml_factory.domain.element import Element
from xml_factory.domain.form_default import FormDefault
from xml_factory.domain.group import Group
from xml_factory.domain.notation import Notation
from xml_factory.domain.simple_type import SimpleType


@dataclass
class Schema:
    target_namespace: str | None = None
    element_form_default: FormDefault = FormDefault.unqualified
    attribute_form_default: FormDefault = FormDefault.unqualified
    elements: dict[str, Element] = field(default_factory=dict)
    simple_types: dict[str, SimpleType] = field(default_factory=dict)
    complex_types: dict[str, ComplexType] = field(default_factory=dict)
    attribute_groups: dict[str, AttributeGroup] = field(default_factory=dict)
    groups: dict[str, Group] = field(default_factory=dict)
    notations: dict[str, Notation] = field(default_factory=dict)
    imports: dict[str, Optional['Schema']] = field(default_factory=dict)
    includes: list['Schema'] = field(default_factory=list)
