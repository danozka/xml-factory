import random
from datetime import timedelta

from xml_factory.domain.restriction import Restriction

from elementpath.datatypes import DateTime10, Timezone


class DateTimeStringValueGenerator:
    RANDOM_MIN_DATE_TIME: DateTime10 = DateTime10(year=1900, month=1, day=1, tzinfo=None)
    RANDOM_MAX_DATE_TIME: DateTime10 = DateTime10(year=2024, month=12, day=31, tzinfo=None)

    def generate_min_date_time_string_value(self, restriction: Restriction) -> str:
        min_inclusive: DateTime10 | None = restriction.min_inclusive
        min_exclusive: DateTime10 | None = restriction.min_exclusive
        if min_inclusive is not None:
            return str(min_inclusive)
        elif min_exclusive is not None:
            return str(min_exclusive + timedelta(microseconds=1))
        else:
            return self.generate_random_date_time_string_value(restriction)

    def generate_max_date_time_string_value(self, restriction: Restriction) -> str:
        max_inclusive: DateTime10 | None = restriction.max_inclusive
        max_exclusive: DateTime10 | None = restriction.max_exclusive
        if max_inclusive is not None:
            return str(max_inclusive)
        elif max_exclusive is not None:
            return str(max_exclusive + timedelta(microseconds=-1))
        else:
            return self.generate_random_date_time_string_value(restriction)

    def generate_random_date_time_string_value(self, restriction: Restriction) -> str:
        min_date_time: DateTime10 = self._get_effective_min_date_time(restriction)
        max_date_time: DateTime10 = self._get_effective_max_date_time(restriction)
        microseconds_between: int = (max_date_time - min_date_time).get_timedelta().microseconds
        if microseconds_between < 0:
            return str(min_date_time)
        random_microseconds: int = random.randint(a=0, b=microseconds_between)
        result: DateTime10 = min_date_time + timedelta(microseconds=random_microseconds)
        time_zone: Timezone | None = self._get_timezone(restriction)
        if time_zone is not None and result.tzinfo is None:
            result = DateTime10(
                year=result.year,
                month=result.month,
                day=result.day,
                hour=result.hour,
                minute=result.minute,
                second=result.second,
                microsecond=result.microsecond,
                tzinfo=time_zone
            )
        return str(result)

    def _get_effective_min_date_time(self, restriction: Restriction) -> DateTime10:
        min_inclusive: DateTime10 | None = restriction.min_inclusive
        min_exclusive: DateTime10 | None = restriction.min_exclusive
        if min_inclusive is not None:
            return min_inclusive
        elif min_exclusive is not None:
            return min_exclusive + timedelta(microseconds=1)
        else:
            return self.RANDOM_MIN_DATE_TIME

    def _get_effective_max_date_time(self, restriction: Restriction) -> DateTime10:
        max_inclusive: DateTime10 | None = restriction.max_inclusive
        max_exclusive: DateTime10 | None = restriction.max_exclusive
        if max_inclusive is not None:
            return max_inclusive
        elif max_exclusive is not None:
            return max_exclusive + timedelta(microseconds=-1)
        else:
            return self.RANDOM_MAX_DATE_TIME

    @staticmethod
    def _get_timezone(restriction: Restriction) -> Timezone | None:
        val: DateTime10 | None
        for val in [
            restriction.min_inclusive,
            restriction.max_inclusive,
            restriction.min_exclusive,
            restriction.max_exclusive
        ]:
            if val is not None and val.tzinfo is not None:
                return val.tzinfo
        return None
