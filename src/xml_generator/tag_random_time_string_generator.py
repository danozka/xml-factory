from datetime import datetime, timezone


class TagRandomTimeStringGenerator:
    _time_string_format: str = '%H:%M:%S'

    def generate_random_time_string_for_tag(self) -> str:
        return datetime.now(timezone.utc).strftime(self._time_string_format)
