import random

from elementpath.datatypes import GregorianYear10, Timezone

from xml_factory.domain.restriction import Restriction


class GregorianYearStringValueGenerator:
    RANDOM_MIN_GREGORIAN_YEAR: GregorianYear10 = GregorianYear10(year=1900, tzinfo=None)
    RANDOM_MAX_GREGORIAN_YEAR: GregorianYear10 = GregorianYear10(year=2024, tzinfo=None)

    def generate_min_gregorian_year_string_value(self, restriction: Restriction) -> str:
        min_inclusive: GregorianYear10 | None = restriction.min_inclusive
        min_exclusive: GregorianYear10 | None = restriction.min_exclusive
        if min_inclusive is not None:
            return str(min_inclusive)
        elif min_exclusive is not None:
            return str(GregorianYear10(year=(min_exclusive.year + 1), tzinfo=min_exclusive.tzinfo))
        else:
            return self.generate_random_gregorian_year_string_value(restriction)

    def generate_max_gregorian_year_string_value(self, restriction: Restriction) -> str:
        max_inclusive: GregorianYear10 | None = restriction.max_inclusive
        max_exclusive: GregorianYear10 | None = restriction.max_exclusive
        if max_inclusive is not None:
            return str(max_inclusive)
        elif max_exclusive is not None:
            return str(GregorianYear10(year=(max_exclusive.year - 1), tzinfo=max_exclusive.tzinfo))
        else:
            return self.generate_random_gregorian_year_string_value(restriction)

    def generate_random_gregorian_year_string_value(self, restriction: Restriction) -> str:
        min_gregorian_year: GregorianYear10 = self._get_effective_min_gregorian_day(restriction)
        max_gregorian_year: GregorianYear10 = self._get_effective_max_gregorian_day(restriction)
        years_between: int = max_gregorian_year.year - min_gregorian_year.year
        if years_between < 0:
            return str(min_gregorian_year)
        random_years: int = random.randint(a=0, b=years_between)
        result: GregorianYear10 = GregorianYear10(
            year=(min_gregorian_year.year + random_years),
            tzinfo=min_gregorian_year.tzinfo
        )
        time_zone: Timezone | None = self._get_timezone(restriction)
        if time_zone is not None and result.tzinfo is None:
            result = GregorianYear10(year=result.year, tzinfo=time_zone)
        return str(result)

    def _get_effective_min_gregorian_day(self, restriction: Restriction) -> GregorianYear10:
        min_inclusive: GregorianYear10 | None = restriction.min_inclusive
        min_exclusive: GregorianYear10 | None = restriction.min_exclusive
        if min_inclusive is not None:
            return min_inclusive
        elif min_exclusive is not None:
            return GregorianYear10(year=(min_exclusive.year + 1), tzinfo=min_exclusive.tzinfo)
        else:
            return self.RANDOM_MIN_GREGORIAN_YEAR

    def _get_effective_max_gregorian_day(self, restriction: Restriction) -> GregorianYear10:
        max_inclusive: GregorianYear10 | None = restriction.max_inclusive
        max_exclusive: GregorianYear10 | None = restriction.max_exclusive
        if max_inclusive is not None:
            return max_inclusive
        elif max_exclusive is not None:
            return GregorianYear10(year=(max_exclusive.year - 1), tzinfo=max_exclusive.tzinfo)
        else:
            return self.RANDOM_MAX_GREGORIAN_YEAR

    @staticmethod
    def _get_timezone(restriction: Restriction) -> Timezone | None:
        val: GregorianYear10 | None
        for val in [
            restriction.min_inclusive,
            restriction.max_inclusive,
            restriction.min_exclusive,
            restriction.max_exclusive
        ]:
            if val is not None and val.tzinfo is not None:
                return val.tzinfo
        return None
