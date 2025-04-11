from datetime import datetime, timezone


class TimeStringValueGenerator:
    _time_string_format: str = '%H:%M:%S'

    def generate_random_time_string_value(self) -> str:
        return datetime.now(timezone.utc).strftime(self._time_string_format)
