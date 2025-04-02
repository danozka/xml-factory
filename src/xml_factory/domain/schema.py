from dataclasses import dataclass, field
from typing import Optional

from xml_factory.domain.element import Element
from xml_factory.domain.form_default import FormDefault


@dataclass
class Schema:
    target_namespace: str | None = None
    element_form_default: FormDefault = FormDefault.unqualified
    attribute_form_default: FormDefault = FormDefault.unqualified
    elements: dict[str, Element] = field(default_factory=dict)
    imports: dict[str, Optional['Schema']] = field(default_factory=dict)
    includes: list['Schema'] = field(default_factory=list)
