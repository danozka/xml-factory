from abc import ABC, abstractmethod

from xml_factory.domain.restriction import Restriction


class IRestrictionPatternValueGenerator(ABC):
    @abstractmethod
    def generate_restriction_pattern_value(self, restriction: Restriction) -> str:
        pass

    @abstractmethod
    def update_patterns(self) -> None:
        pass
