import random
from datetime import timedelta

from elementpath.datatypes import Date10, Timezone

from xml_factory.domain.restriction import Restriction


class DateStringValueGenerator:
    RANDOM_MIN_DATE: Date10 = Date10(year=1900, month=1, day=1, tzinfo=None)
    RANDOM_MAX_DATE: Date10 = Date10(year=2024, month=12, day=31, tzinfo=None)

    def generate_min_date_string_value(self, restriction: Restriction) -> str:
        min_inclusive: Date10 | None = restriction.min_inclusive
        min_exclusive: Date10 | None = restriction.min_exclusive
        if min_inclusive is not None:
            return str(min_inclusive)
        elif min_exclusive is not None:
            return str(min_exclusive + timedelta(days=1))
        else:
            return self.generate_random_date_string_value(restriction)

    def generate_max_date_string_value(self, restriction: Restriction) -> str:
        max_inclusive: Date10 | None = restriction.max_inclusive
        max_exclusive: Date10 | None = restriction.max_exclusive
        if max_inclusive is not None:
            return str(max_inclusive)
        elif max_exclusive is not None:
            return str(max_exclusive + timedelta(days=-1))
        else:
            return self.generate_random_date_string_value(restriction)

    def generate_random_date_string_value(self, restriction: Restriction) -> str:
        min_date: Date10 = self._get_effective_min_date(restriction)
        max_date: Date10 = self._get_effective_max_date(restriction)
        days_between: int = (max_date - min_date).get_timedelta().days
        if days_between < 0:
            return str(min_date)
        random_days: int = random.randint(a=0, b=days_between)
        result: Date10 = min_date + timedelta(days=random_days)
        time_zone: Timezone | None = self._get_timezone(restriction)
        if time_zone is not None and result.tzinfo is None:
            result = Date10(year=result.year, month=result.month, day=result.day, tzinfo=time_zone)
        return str(result)

    def _get_effective_min_date(self, restriction: Restriction) -> Date10:
        min_inclusive: Date10 | None = restriction.min_inclusive
        min_exclusive: Date10 | None = restriction.min_exclusive
        if min_inclusive is not None:
            return min_inclusive
        elif min_exclusive is not None:
            return min_exclusive + timedelta(days=1)
        else:
            return self.RANDOM_MIN_DATE

    def _get_effective_max_date(self, restriction: Restriction) -> Date10:
        max_inclusive: Date10 | None = restriction.max_inclusive
        max_exclusive: Date10 | None = restriction.max_exclusive
        if max_inclusive is not None:
            return max_inclusive
        elif max_exclusive is not None:
            return max_exclusive + timedelta(days=-1)
        else:
            return self.RANDOM_MAX_DATE

    @staticmethod
    def _get_timezone(restriction: Restriction) -> Timezone | None:
        val: Date10 | None
        for val in [
            restriction.min_inclusive,
            restriction.max_inclusive,
            restriction.min_exclusive,
            restriction.max_exclusive
        ]:
            if val is not None and val.tzinfo is not None:
                return val.tzinfo
        return None
