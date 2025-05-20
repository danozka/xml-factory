from abc import ABC, abstractmethod

from xml_factory.domain.restriction import Restriction


class IListNumberOfItemsGetter(ABC):
    @abstractmethod
    def get_list_number_of_items(self, list_restriction: Restriction) -> int:
        pass
