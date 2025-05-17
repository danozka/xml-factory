import random
from datetime import datetime, timedelta

from elementpath.datatypes import GregorianMonthDay, Timezone

from xml_factory.domain.restriction import Restriction


class GregorianMonthDayStringValueGenerator:
    RANDOM_MIN_GREGORIAN_MONTH_DAY: GregorianMonthDay = GregorianMonthDay(month=1, day=1, tzinfo=None)
    RANDOM_MAX_GREGORIAN_MONTH_DAY: GregorianMonthDay = GregorianMonthDay(month=12, day=31, tzinfo=None)

    def generate_min_gregorian_month_day_string_value(self, restriction: Restriction) -> str:
        min_inclusive: GregorianMonthDay | None = restriction.min_inclusive
        min_exclusive: GregorianMonthDay | None = restriction.min_exclusive
        if min_inclusive is not None:
            return str(min_inclusive)
        elif min_exclusive is not None:
            return str(self._next_month_day(min_exclusive))
        else:
            return self.generate_random_gregorian_month_day_string_value(restriction)

    def generate_max_gregorian_month_day_string_value(self, restriction: Restriction) -> str:
        max_inclusive: GregorianMonthDay | None = restriction.max_inclusive
        max_exclusive: GregorianMonthDay | None = restriction.max_exclusive
        if max_inclusive is not None:
            return str(max_inclusive)
        elif max_exclusive is not None:
            return str(self._previous_month_day(max_exclusive))
        else:
            return self.generate_random_gregorian_month_day_string_value(restriction)

    def generate_random_gregorian_month_day_string_value(self, restriction: Restriction) -> str:
        min_gregorian_month_day: GregorianMonthDay = self._get_effective_min_gregorian_month_day(restriction)
        max_gregorian_month_day: GregorianMonthDay = self._get_effective_max_gregorian_month_day(restriction)
        days_between: int = (max_gregorian_month_day - max_gregorian_month_day).get_timedelta().days
        if days_between < 0:
            return str(min_gregorian_month_day)
        random_days: int = random.randint(a=0, b=days_between)
        random_date_time: datetime = (
            datetime(year=2025, month=min_gregorian_month_day.month, day=min_gregorian_month_day.day) +
            timedelta(days=random_days)
        )
        result: GregorianMonthDay = GregorianMonthDay(
            month=random_date_time.month,
            day=random_date_time.day,
            tzinfo=min_gregorian_month_day.tzinfo
        )
        time_zone: Timezone | None = self._get_timezone(restriction)
        if time_zone is not None and result.tzinfo is None:
            result = GregorianMonthDay(month=result.month, day=result.day, tzinfo=time_zone)
        return str(result)

    def _get_effective_min_gregorian_month_day(self, restriction: Restriction) -> GregorianMonthDay:
        min_inclusive: GregorianMonthDay | None = restriction.min_inclusive
        min_exclusive: GregorianMonthDay | None = restriction.min_exclusive
        if min_inclusive is not None:
            return min_inclusive
        elif min_exclusive is not None:
            return self._next_month_day(min_exclusive)
        else:
            return self.RANDOM_MIN_GREGORIAN_MONTH_DAY

    def _get_effective_max_gregorian_month_day(self, restriction: Restriction) -> GregorianMonthDay:
        max_inclusive: GregorianMonthDay | None = restriction.max_inclusive
        max_exclusive: GregorianMonthDay | None = restriction.max_exclusive
        if max_inclusive is not None:
            return max_inclusive
        elif max_exclusive is not None:
            return self._previous_month_day(max_exclusive)
        else:
            return self.RANDOM_MAX_GREGORIAN_MONTH_DAY

    @staticmethod
    def _get_timezone(restriction: Restriction) -> Timezone | None:
        val: GregorianMonthDay | None
        for val in [
            restriction.min_inclusive,
            restriction.max_inclusive,
            restriction.min_exclusive,
            restriction.max_exclusive
        ]:
            if val is not None and val.tzinfo is not None:
                return val.tzinfo
        return None

    @staticmethod
    def _days_in_month(month: int) -> int:
        if month == 2:
            return 29
        elif month in {4, 6, 9, 11}:
            return 30
        return 31

    def _next_month_day(self, month_day: GregorianMonthDay) -> GregorianMonthDay:
        days_in_month: int = self._days_in_month(month_day.month)
        if month_day.day < days_in_month:
            return GregorianMonthDay(month=month_day.month, day=(month_day.day + 1), tzinfo=month_day.tzinfo)
        if month_day.month < 12:
            return GregorianMonthDay(month=(month_day.month + 1), day=1, tzinfo=month_day.tzinfo)
        return self.RANDOM_MAX_GREGORIAN_MONTH_DAY

    def _previous_month_day(self, month_day: GregorianMonthDay) -> GregorianMonthDay:
        if month_day.day > 1:
            return GregorianMonthDay(month=month_day.month, day=(month_day.day -1), tzinfo=month_day.tzinfo)
        if month_day.month > 1:
            previous_month: int = month_day.month - 1
            return GregorianMonthDay(
                month=previous_month,
                day=self._days_in_month(previous_month),
                tzinfo=month_day.tzinfo
            )
        return self.RANDOM_MIN_GREGORIAN_MONTH_DAY
