from xmlschema.validators import XsdElement, XsdGroup

from xml_factory.complex.i_group_content_number_of_occurrences_getter import IGroupContentNumberOfOccurrencesGetter


class GroupContentMinNumberOfOccurrencesGetter(IGroupContentNumberOfOccurrencesGetter):
    def get_group_content_number_of_occurrences(self, group_content: XsdElement | XsdGroup) -> int:
        return group_content.min_occurs
