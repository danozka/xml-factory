from abc import ABC, abstractmethod

from xml_factory.domain.restriction import Restriction


class IRestrictionValueGenerator(ABC):
    @abstractmethod
    def generate_restriction_value(self, restriction: Restriction) -> str:
        pass
