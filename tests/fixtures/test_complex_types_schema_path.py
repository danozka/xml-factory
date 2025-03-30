from pathlib import Path

import pytest


@pytest.fixture(scope='session')
def test_complex_types_schema_path() -> Path:
    return Path(__file__).parent.joinpath('test_complex_types_schema.xsd')
