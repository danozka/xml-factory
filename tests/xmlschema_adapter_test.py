from pathlib import Path

import pytest
from xmlschema import XMLSchema as XmlschemaSchema

from adapters.xmlschema_adapter import XmlschemaAdapter
from xml_factory.domain.xsd_simple_type import XsdSimpleType


@pytest.fixture(scope='function')
def xmlschema_adapter() -> XmlschemaAdapter:
    return XmlschemaAdapter()


def test_simple_types_are_adapted(xmlschema_adapter: XmlschemaAdapter, test_simple_types_schema_path: Path) -> None:
    xmlschema_schema: XmlschemaSchema = XmlschemaSchema(test_simple_types_schema_path)
    result: list[XsdSimpleType] = [
        xmlschema_adapter.adapt_xmlschema_simple_type(x) for x in xmlschema_schema.simple_types
    ]
    assert True
