import random

from xml_factory.domain.restriction import Restriction
from xml_factory.simple.i_list_number_of_items_getter import IListNumberOfItemsGetter


class ListRandomNumberOfItemsGetter(IListNumberOfItemsGetter):
    _unbounded_length: int

    def __init__(self, unbounded_length: int) -> None:
        self._unbounded_length = unbounded_length

    def get_list_number_of_items(self, list_restriction: Restriction) -> int:
        if list_restriction.length is not None:
            return list_restriction.length
        else:
            min_length: int = list_restriction.min_length if list_restriction.min_length is not None else 1
            max_length: int = (
                max(min_length, self._unbounded_length)
                if list_restriction.max_length is None else list_restriction.max_length
            )
            return random.randint(a=min_length, b=max_length)
