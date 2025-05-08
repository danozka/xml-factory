from abc import ABC, abstractmethod

from xmlschema.validators import XsdElement, XsdGroup


class IGroupContentNumberOfOccurrencesGetter(ABC):
    @abstractmethod
    def get_group_content_number_of_occurrences(self, group_content: XsdElement | XsdGroup) -> int:
        pass
