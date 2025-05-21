from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class JsonPattern(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)
    pattern: str
    value: str
    length: int | None = None
    min_length: int | None = None
    max_length: int | None = None

    def __str__(self) -> str:
        return self.__repr__()
