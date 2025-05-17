import random
from datetime import timedelta

from elementpath.datatypes import Time, Timezone

from xml_factory.domain.restriction import Restriction


class TimeStringValueGenerator:
    RANDOM_MIN_TIME: Time = Time(hour=0, minute=0, second=0, microsecond=0, tzinfo=None)
    RANDOM_MAX_TIME: Time = Time(hour=23, minute=59, second=59, microsecond=999999, tzinfo=None)

    def generate_min_time_string_value(self, restriction: Restriction) -> str:
        min_inclusive: Time | None = restriction.min_inclusive
        min_exclusive: Time | None = restriction.min_exclusive
        if min_inclusive is not None:
            return str(min_inclusive)
        elif min_exclusive is not None:
            return str(min_exclusive + timedelta(microseconds=1))
        else:
            return self.generate_random_time_string_value(restriction)

    def generate_max_time_string_value(self, restriction: Restriction) -> str:
        max_inclusive: Time | None = restriction.max_inclusive
        max_exclusive: Time | None = restriction.max_exclusive
        if max_inclusive is not None:
            return str(max_inclusive)
        elif max_exclusive is not None:
            return str(max_exclusive + timedelta(microseconds=-1))
        else:
            return self.generate_random_time_string_value(restriction)

    def generate_random_time_string_value(self, restriction: Restriction) -> str:
        min_time: Time = self._get_effective_min_time(restriction)
        max_time: Time = self._get_effective_max_time(restriction)
        microseconds_between: int = (max_time - min_time).get_timedelta().microseconds
        if microseconds_between < 0:
            return str(min_time)
        random_microseconds: int = random.randint(a=0, b=microseconds_between)
        result: Time = min_time + timedelta(microseconds=random_microseconds)
        time_zone: Timezone | None = self._get_timezone(restriction)
        if time_zone is not None and result.tzinfo is None:
            result = Time(
                hour=result.hour,
                minute=result.minute,
                second=result.second,
                microsecond=result.microsecond,
                tzinfo=time_zone
            )
        return str(result)

    def _get_effective_min_time(self, restriction: Restriction) -> Time:
        min_inclusive: Time | None = restriction.min_inclusive
        min_exclusive: Time | None = restriction.min_exclusive
        if min_inclusive is not None:
            return min_inclusive
        elif min_exclusive is not None:
            return min_exclusive + timedelta(microseconds=1)
        else:
            return self.RANDOM_MIN_TIME

    def _get_effective_max_time(self, restriction: Restriction) -> Time:
        max_inclusive: Time | None = restriction.max_inclusive
        max_exclusive: Time | None = restriction.max_exclusive
        if max_inclusive is not None:
            return max_inclusive
        elif max_exclusive is not None:
            return max_exclusive + timedelta(microseconds=-1)
        else:
            return self.RANDOM_MAX_TIME

    @staticmethod
    def _get_timezone(restriction: Restriction) -> Timezone | None:
        val: Time | None
        for val in [
            restriction.min_inclusive,
            restriction.max_inclusive,
            restriction.min_exclusive,
            restriction.max_exclusive
        ]:
            if val is not None and val.tzinfo is not None:
                return val.tzinfo
        return None
