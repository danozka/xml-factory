from pathlib import Path

import pytest


@pytest.fixture(scope='session')
def test_schema_path() -> Path:
    return Path(__file__).parent.joinpath('test_schema.xsd')
