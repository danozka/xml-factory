from pathlib import Path

import pytest


@pytest.fixture(scope='session')
def test_simple_types_schema_path() -> Path:
    return Path(__file__).parent.joinpath('test_simple_types_schema.xsd')
