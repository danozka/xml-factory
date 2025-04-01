from dataclasses import dataclass

from xml_factory.domain.component import Component


@dataclass
class Notation(Component):
    system: str | None = None
    public: str | None = None
