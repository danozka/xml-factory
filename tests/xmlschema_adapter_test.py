from pathlib import Path

import pytest
from xmlschema import XMLSchema as XmlschemaSchema

from adapters.xmlschema_adapter import XmlschemaAdapter
from xml_factory.domain.complex_type import ComplexType
from xml_factory.domain.simple_type import SimpleType


@pytest.fixture(scope='function')
def xmlschema_adapter() -> XmlschemaAdapter:
    return XmlschemaAdapter()


def test_simple_types_are_adapted(xmlschema_adapter: XmlschemaAdapter, test_simple_types_schema_path: Path) -> None:
    xmlschema_schema: XmlschemaSchema = XmlschemaSchema(test_simple_types_schema_path)
    result: list[SimpleType] = [
        xmlschema_adapter.adapt_xmlschema_simple_type(x) for x in xmlschema_schema.simple_types
    ]
    assert all([isinstance(x, SimpleType) for x in result])


def test_complex_types_are_adapted(xmlschema_adapter: XmlschemaAdapter, test_complex_types_schema_path: Path) -> None:
    xmlschema_schema: XmlschemaSchema = XmlschemaSchema(test_complex_types_schema_path)
    result: list[ComplexType] = [
        xmlschema_adapter.adapt_xmlschema_complex_type(x) for x in xmlschema_schema.complex_types
    ]
    assert all([isinstance(x, ComplexType) for x in result])
