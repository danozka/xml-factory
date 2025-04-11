from datetime import datetime, timezone


class DateTimeStringValueGenerator:
    _date_time_string_format: str = '%Y-%m-%dT%H:%M:%S.%f'

    def generate_random_date_time_string_value(self) -> str:
        return datetime.now(timezone.utc).strftime(self._date_time_string_format)[:-3]
