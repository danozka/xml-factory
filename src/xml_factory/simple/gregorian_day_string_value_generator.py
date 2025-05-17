import random

from elementpath.datatypes import GregorianDay, Timezone

from xml_factory.domain.restriction import Restriction


class GregorianDayStringValueGenerator:
    RANDOM_MIN_GREGORIAN_DAY: GregorianDay = GregorianDay(day=1, tzinfo=None)
    RANDOM_MAX_GREGORIAN_DAY: GregorianDay = GregorianDay(day=31, tzinfo=None)

    def generate_min_gregorian_day_string_value(self, restriction: Restriction) -> str:
        min_inclusive: GregorianDay | None = restriction.min_inclusive
        min_exclusive: GregorianDay | None = restriction.min_exclusive
        if min_inclusive is not None:
            return str(min_inclusive)
        elif min_exclusive is not None:
            return str(GregorianDay(day=(min_exclusive.day + 1), tzinfo=min_exclusive.tzinfo))
        else:
            return self.generate_random_gregorian_day_string_value(restriction)

    def generate_max_gregorian_day_string_value(self, restriction: Restriction) -> str:
        max_inclusive: GregorianDay | None = restriction.max_inclusive
        max_exclusive: GregorianDay | None = restriction.max_exclusive
        if max_inclusive is not None:
            return str(max_inclusive)
        elif max_exclusive is not None:
            return str(GregorianDay(day=(max_exclusive.day - 1), tzinfo=max_exclusive.tzinfo))
        else:
            return self.generate_random_gregorian_day_string_value(restriction)

    def generate_random_gregorian_day_string_value(self, restriction: Restriction) -> str:
        min_gregorian_day: GregorianDay = self._get_effective_min_gregorian_day(restriction)
        max_gregorian_day: GregorianDay = self._get_effective_max_gregorian_day(restriction)
        days_between: int = max_gregorian_day.day - min_gregorian_day.day
        if days_between < 0:
            return str(min_gregorian_day)
        random_days: int = random.randint(a=0, b=days_between)
        result: GregorianDay = GregorianDay(day=(min_gregorian_day.day + random_days), tzinfo=min_gregorian_day.tzinfo)
        time_zone: Timezone | None = self._get_timezone(restriction)
        if time_zone is not None and result.tzinfo is None:
            result = GregorianDay(day=result.day, tzinfo=time_zone)
        return str(result)

    def _get_effective_min_gregorian_day(self, restriction: Restriction) -> GregorianDay:
        min_inclusive: GregorianDay | None = restriction.min_inclusive
        min_exclusive: GregorianDay | None = restriction.min_exclusive
        if min_inclusive is not None:
            return min_inclusive
        elif min_exclusive is not None:
            return GregorianDay(day=(min_exclusive.day + 1), tzinfo=min_exclusive.tzinfo)
        else:
            return self.RANDOM_MIN_GREGORIAN_DAY

    def _get_effective_max_gregorian_day(self, restriction: Restriction) -> GregorianDay:
        max_inclusive: GregorianDay | None = restriction.max_inclusive
        max_exclusive: GregorianDay | None = restriction.max_exclusive
        if max_inclusive is not None:
            return max_inclusive
        elif max_exclusive is not None:
            return GregorianDay(day=(max_exclusive.day - 1), tzinfo=max_exclusive.tzinfo)
        else:
            return self.RANDOM_MAX_GREGORIAN_DAY

    @staticmethod
    def _get_timezone(restriction: Restriction) -> Timezone | None:
        val: GregorianDay | None
        for val in [
            restriction.min_inclusive,
            restriction.max_inclusive,
            restriction.min_exclusive,
            restriction.max_exclusive
        ]:
            if val is not None and val.tzinfo is not None:
                return val.tzinfo
        return None
