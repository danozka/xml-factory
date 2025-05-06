import tempfile
from pathlib import Path
from typing import Generator

import pytest

from xml_factory.xml_generator import XmlGenerator


@pytest.fixture(scope='function')
def xml_generator() -> XmlGenerator:
    return XmlGenerator()


@pytest.fixture(scope='function')
def test_xml_path() -> Generator[Path, None, None]:
    xml_path: Path = Path(tempfile.gettempdir()).joinpath('test_output.xml')
    yield xml_path
    if xml_path.is_file():
        xml_path.unlink()


def test_xml_is_generated(
    xml_generator: XmlGenerator,
    test_complex_types_schema_path: Path,
    test_xml_path: Path
) -> None:
    exit_code: int = xml_generator.generate_xml(
        xsd_path=test_complex_types_schema_path,
        xml_path=test_xml_path,
        root_element_name='Company'
    )
    assert exit_code == 0
