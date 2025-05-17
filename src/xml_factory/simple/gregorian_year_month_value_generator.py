import random

from elementpath.datatypes import GregorianYearMonth10, Timezone

from xml_factory.domain.restriction import Restriction


class GregorianYearMonthStringValueGenerator:
    RANDOM_MIN_GREGORIAN_YEAR_MONTH: GregorianYearMonth10 = GregorianYearMonth10(year=1970, month=1, tzinfo=None)
    RANDOM_MAX_GREGORIAN_YEAR_MONTH: GregorianYearMonth10 = GregorianYearMonth10(year=2050, month=12, tzinfo=None)

    def generate_min_gregorian_year_month_string_value(self, restriction: Restriction) -> str:
        min_inclusive: GregorianYearMonth10 | None = restriction.min_inclusive
        min_exclusive: GregorianYearMonth10 | None = restriction.min_exclusive
        if min_inclusive is not None:
            return str(min_inclusive)
        elif min_exclusive is not None:
            return str(self._next_year_month(min_exclusive))
        else:
            return self.generate_random_gregorian_year_month_string_value(restriction)

    def generate_max_gregorian_year_month_string_value(self, restriction: Restriction) -> str:
        max_inclusive: GregorianYearMonth10 | None = restriction.max_inclusive
        max_exclusive: GregorianYearMonth10 | None = restriction.max_exclusive
        if max_inclusive is not None:
            return str(max_inclusive)
        elif max_exclusive is not None:
            return str(self._previous_year_month(max_exclusive))
        else:
            return self.generate_random_gregorian_year_month_string_value(restriction)

    def generate_random_gregorian_year_month_string_value(self, restriction: Restriction) -> str:
        min_gregorian_year_month: GregorianYearMonth10 = self._get_effective_min_gregorian_year_month(restriction)
        max_gregorian_year_month: GregorianYearMonth10 = self._get_effective_max_gregorian_year_month(restriction)
        min_total_months: int = min_gregorian_year_month.year * 12 + min_gregorian_year_month.month
        max_total_months: int = max_gregorian_year_month.year * 12 + max_gregorian_year_month.month
        months_between: int = max_total_months - min_total_months
        if months_between < 0:
            return str(min_gregorian_year_month)
        random_months: int = random.randint(a=0, b=months_between)
        random_total_months: int = min_total_months + random_months
        year: int = random_total_months // 12
        month: int = random_total_months % 12
        if month == 0:
            month = 12
            year -= 1
        result: GregorianYearMonth10 = GregorianYearMonth10(
            year=year,
            month=month,
            tzinfo=min_gregorian_year_month.tzinfo
        )
        time_zone: Timezone | None = self._get_timezone(restriction)
        if time_zone is not None and result.tzinfo is None:
            result = GregorianYearMonth10(year=result.year, month=result.month, tzinfo=time_zone)
        return str(result)

    def _get_effective_min_gregorian_year_month(self, restriction: Restriction) -> GregorianYearMonth10:
        min_inclusive: GregorianYearMonth10 | None = restriction.min_inclusive
        min_exclusive: GregorianYearMonth10 | None = restriction.min_exclusive
        if min_inclusive is not None:
            return min_inclusive
        elif min_exclusive is not None:
            return self._next_year_month(min_exclusive)
        else:
            return self.RANDOM_MIN_GREGORIAN_YEAR_MONTH

    def _get_effective_max_gregorian_year_month(self, restriction: Restriction) -> GregorianYearMonth10:
        max_inclusive: GregorianYearMonth10 | None = restriction.max_inclusive
        max_exclusive: GregorianYearMonth10 | None = restriction.max_exclusive
        if max_inclusive is not None:
            return max_inclusive
        elif max_exclusive is not None:
            return self._previous_year_month(max_exclusive)
        else:
            return self.RANDOM_MAX_GREGORIAN_YEAR_MONTH

    @staticmethod
    def _get_timezone(restriction: Restriction) -> Timezone | None:
        val: GregorianYearMonth10 | None
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
    def _next_year_month(year_month: GregorianYearMonth10) -> GregorianYearMonth10:
        if year_month.month < 12:
            return GregorianYearMonth10(year=year_month.year, month=(year_month.month + 1), tzinfo=year_month.tzinfo)
        return GregorianYearMonth10(year=(year_month.year + 1), month=1, tzinfo=year_month.tzinfo)

    @staticmethod
    def _previous_year_month(year_month: GregorianYearMonth10) -> GregorianYearMonth10:
        if year_month.month > 1:
            return GregorianYearMonth10(year=year_month.year, month=(year_month.month - 1), tzinfo=year_month.tzinfo)
        return GregorianYearMonth10(year=(year_month.year - 1), month=12, tzinfo=year_month.tzinfo)