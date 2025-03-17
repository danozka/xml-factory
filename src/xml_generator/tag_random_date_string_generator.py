from datetime import datetime, timezone


class TagRandomDateStringGenerator:
    _date_string_format: str = '%Y-%m-%d'

    def generate_random_date_string_for_tag(self) -> str:
        return datetime.now(timezone.utc).strftime(self._date_string_format)
