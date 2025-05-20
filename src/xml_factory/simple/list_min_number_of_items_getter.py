from xml_factory.domain.restriction import Restriction
from xml_factory.simple.i_list_number_of_items_getter import IListNumberOfItemsGetter


class ListMinNumberOfItemsGetter(IListNumberOfItemsGetter):
    def get_list_number_of_items(self, list_restriction: Restriction) -> int:
        if list_restriction.length is not None:
            return list_restriction.length
        else:
            min_length: int = list_restriction.min_length if list_restriction.min_length is not None else 1
            return min_length
