from xmlschema.validators import XsdElement, XsdGroup

from xml_factory.complex.i_group_content_number_of_occurrences_getter import IGroupContentNumberOfOccurrencesGetter


class GroupContentMaxNumberOfOccurrencesGetter(IGroupContentNumberOfOccurrencesGetter):
    _unbounded_occurs: int

    def __init__(self, unbounded_occurs: int) -> None:
        self._unbounded_occurs = unbounded_occurs

    def get_group_content_number_of_occurrences(self, group_content: XsdElement | XsdGroup) -> int:
        return (
            max(group_content.min_occurs, self._unbounded_occurs)
            if group_content.max_occurs is None else group_content.max_occurs
        )
