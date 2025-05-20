from xml_factory.domain.restriction import Restriction
from xml_factory.simple.i_list_number_of_items_getter import IListNumberOfItemsGetter


class ListMaxNumberOfItemsGetter(IListNumberOfItemsGetter):
    _unbounded_length: int

    def __init__(self, unbounded_length: int) -> None:
        self._unbounded_length = unbounded_length

    def get_list_number_of_items(self, list_restriction: Restriction) -> int:
        if list_restriction.length is not None:
            return list_restriction.length
        elif list_restriction.max_length is not None:
            return list_restriction.max_length
        else:
            min_length: int = list_restriction.min_length if list_restriction.min_length is not None else 1
            return max(min_length, self._unbounded_length)
