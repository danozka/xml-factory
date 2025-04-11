from datetime import datetime, timezone


class DateStringValueGenerator:
    _date_string_format: str = '%Y-%m-%d'

    def generate_random_date_string_value(self) -> str:
        return datetime.now(timezone.utc).strftime(self._date_string_format)
