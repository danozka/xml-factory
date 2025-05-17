import random

from elementpath.datatypes import GregorianMonth, Timezone

from xml_factory.domain.restriction import Restriction


class GregorianMonthStringValueGenerator:
    RANDOM_MIN_GREGORIAN_MONTH: GregorianMonth = GregorianMonth(month=1, tzinfo=None)
    RANDOM_MAX_GREGORIAN_MONTH: GregorianMonth = GregorianMonth(month=12, tzinfo=None)

    def generate_min_gregorian_month_string_value(self, restriction: Restriction) -> str:
        min_inclusive: GregorianMonth | None = restriction.min_inclusive
        min_exclusive: GregorianMonth | None = restriction.min_exclusive
        if min_inclusive is not None:
            return str(min_inclusive)
        elif min_exclusive is not None:
            return str(GregorianMonth(month=(min_exclusive.month + 1), tzinfo=min_exclusive.tzinfo))
        else:
            return self.generate_random_gregorian_month_string_value(restriction)

    def generate_max_gregorian_month_string_value(self, restriction: Restriction) -> str:
        max_inclusive: GregorianMonth | None = restriction.max_inclusive
        max_exclusive: GregorianMonth | None = restriction.max_exclusive
        if max_inclusive is not None:
            return str(max_inclusive)
        elif max_exclusive is not None:
            return str(GregorianMonth(month=(max_exclusive.month - 1), tzinfo=max_exclusive.tzinfo))
        else:
            return self.generate_random_gregorian_month_string_value(restriction)

    def generate_random_gregorian_month_string_value(self, restriction: Restriction) -> str:
        min_gregorian_month: GregorianMonth = self._get_effective_min_gregorian_month(restriction)
        max_gregorian_month: GregorianMonth = self._get_effective_max_gregorian_month(restriction)
        months_between: int = max_gregorian_month.month - min_gregorian_month.month
        if months_between < 0:
            return str(min_gregorian_month)
        random_months: int = random.randint(a=0, b=months_between)
        result: GregorianMonth = GregorianMonth(
            month=(min_gregorian_month.month + random_months),
            tzinfo=min_gregorian_month.tzinfo
        )
        time_zone: Timezone | None = self._get_timezone(restriction)
        if time_zone is not None and result.tzinfo is None:
            result = GregorianMonth(month=result.month, tzinfo=time_zone)
        return str(result)

    def _get_effective_min_gregorian_month(self, restriction: Restriction) -> GregorianMonth:
        min_inclusive: GregorianMonth | None = restriction.min_inclusive
        min_exclusive: GregorianMonth | None = restriction.min_exclusive
        if min_inclusive is not None:
            return min_inclusive
        elif min_exclusive is not None:
            return GregorianMonth(month=(min_exclusive.month + 1), tzinfo=min_exclusive.tzinfo)
        else:
            return self.RANDOM_MIN_GREGORIAN_MONTH

    def _get_effective_max_gregorian_month(self, restriction: Restriction) -> GregorianMonth:
        max_inclusive: GregorianMonth | None = restriction.max_inclusive
        max_exclusive: GregorianMonth | None = restriction.max_exclusive
        if max_inclusive is not None:
            return max_inclusive
        elif max_exclusive is not None:
            return GregorianMonth(month=(max_exclusive.month - 1), tzinfo=max_exclusive.tzinfo)
        else:
            return self.RANDOM_MAX_GREGORIAN_MONTH

    @staticmethod
    def _get_timezone(restriction: Restriction) -> Timezone | None:
        val: GregorianMonth | None
        for val in [
            restriction.min_inclusive,
            restriction.max_inclusive,
            restriction.min_exclusive,
            restriction.max_exclusive
        ]:
            if val is not None and val.tzinfo is not None:
                return val.tzinfo
        return None
