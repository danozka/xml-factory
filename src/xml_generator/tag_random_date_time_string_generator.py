from datetime import datetime, timezone


class TagRandomDateTimeStringGenerator:
    _date_time_string_format: str = '%Y-%m-%dT%H:%M:%S.%f'

    def generate_random_date_time_string_for_tag(self) -> str:
        return datetime.now(timezone.utc).strftime(self._date_time_string_format)[:-3]
