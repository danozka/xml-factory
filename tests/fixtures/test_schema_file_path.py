from pathlib import Path

import pytest


@pytest.fixture(scope='session')
def test_schema_file_path() -> Path:
    return Path(__file__).parent.joinpath('files/test_schema.xsd')
