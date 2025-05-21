from pathlib import Path
from typing import Generator
from xml.etree.ElementTree import Element, ElementTree

import pytest

from json_patterns import JsonFileRestrictionPatternValueGenerator
from xml_factory import (
    GroupContentAtLeastOneNumberOfOccurrencesGetter,
    GroupContentMaxNumberOfOccurrencesGetter,
    GroupContentMinNumberOfOccurrencesGetter,
    GroupContentRandomNumberOfOccurrencesGetter,
    ListMaxNumberOfItemsGetter,
    ListMinNumberOfItemsGetter,
    ListRandomNumberOfItemsGetter,
    RestrictionMaxValueGenerator,
    RestrictionMinValueGenerator,
    RestrictionRandomValueGenerator,
    XmlGenerator
)


@pytest.fixture
def temp_xml_path(tmp_path: Path) -> Generator[Path, None, None]:
    temp_xml_path: Path = tmp_path / 'result.xml'
    yield temp_xml_path
    if temp_xml_path.exists():
        temp_xml_path.unlink()


def assert_xml_result(xml_generator: XmlGenerator, xsd_path: Path, xml_path: Path) -> None:
    exit_code: int = xml_generator.generate_xml(xsd_path=xsd_path, xml_path=xml_path, root_element_name='PurchaseOrder')
    assert exit_code == 0
    assert xml_path.exists()
    assert xml_path.stat().st_size > 0


def get_xml_root_element(xml_path: Path) -> Element:
    tree: ElementTree = ElementTree(file=xml_path)
    return tree.getroot()


def test_generate_xml_random(test_schema_file_path: Path, test_patterns_file_path: Path, temp_xml_path: Path) -> None:
    xml_generator: XmlGenerator = XmlGenerator(
        group_content_number_of_occurrences_getter=GroupContentRandomNumberOfOccurrencesGetter(unbounded_occurs=3),
        list_number_of_items_getter=ListRandomNumberOfItemsGetter(unbounded_length=3),
        restriction_pattern_value_generator=JsonFileRestrictionPatternValueGenerator(test_patterns_file_path),
        restriction_value_generator=RestrictionRandomValueGenerator(),
        force_default_value=False
    )
    assert_xml_result(xml_generator=xml_generator, xsd_path=test_schema_file_path, xml_path=temp_xml_path)
    root: Element = get_xml_root_element(temp_xml_path)
    assert 'orderDate' in root.attrib
    assert 'id' in root.attrib
    assert 'priority' in root.attrib
    assert root.find('OrderInfo') is not None
    assert root.find('Customer') is not None
    assert root.find('Items') is not None


def test_generate_xml_min_occurs(
    test_schema_file_path: Path,
    test_patterns_file_path: Path,
    temp_xml_path: Path
) -> None:
    xml_generator: XmlGenerator = XmlGenerator(
        group_content_number_of_occurrences_getter=GroupContentMinNumberOfOccurrencesGetter(),
        list_number_of_items_getter=ListRandomNumberOfItemsGetter(unbounded_length=3),
        restriction_pattern_value_generator=JsonFileRestrictionPatternValueGenerator(test_patterns_file_path),
        restriction_value_generator=RestrictionRandomValueGenerator(),
        force_default_value=False
    )
    assert_xml_result(xml_generator=xml_generator, xsd_path=test_schema_file_path, xml_path=temp_xml_path)
    root: Element = get_xml_root_element(temp_xml_path)
    assert root.find('Payment') is None
    assert root.find('Notes') is None
    items: Element | None = root.find('Items')
    assert items is not None
    assert len(items.findall('Item')) >= 1


def test_generate_xml_max_occurs(
    test_schema_file_path: Path,
    test_patterns_file_path: Path,
    temp_xml_path: Path
) -> None:
    xml_generator: XmlGenerator = XmlGenerator(
        group_content_number_of_occurrences_getter=GroupContentMaxNumberOfOccurrencesGetter(unbounded_occurs=5),
        list_number_of_items_getter=ListRandomNumberOfItemsGetter(unbounded_length=3),
        restriction_pattern_value_generator=JsonFileRestrictionPatternValueGenerator(test_patterns_file_path),
        restriction_value_generator=RestrictionRandomValueGenerator(),
        force_default_value=False
    )
    assert_xml_result(xml_generator=xml_generator, xsd_path=test_schema_file_path, xml_path=temp_xml_path)
    root: Element = get_xml_root_element(temp_xml_path)
    notes: list[Element] = root.findall('Notes')
    assert notes is not None
    items: Element | None = root.find('Items')
    assert items is not None
    assert len(items.findall('Item')) <= 5


def test_generate_xml_at_least_one(
    test_schema_file_path: Path,
    test_patterns_file_path: Path,
    temp_xml_path: Path
) -> None:
    xml_generator: XmlGenerator = XmlGenerator(
        group_content_number_of_occurrences_getter=GroupContentAtLeastOneNumberOfOccurrencesGetter(),
        list_number_of_items_getter=ListRandomNumberOfItemsGetter(unbounded_length=3),
        restriction_pattern_value_generator=JsonFileRestrictionPatternValueGenerator(test_patterns_file_path),
        restriction_value_generator=RestrictionRandomValueGenerator(),
        force_default_value=False
    )
    assert_xml_result(xml_generator=xml_generator, xsd_path=test_schema_file_path, xml_path=temp_xml_path)
    root: Element = get_xml_root_element(temp_xml_path)
    assert root.find('Payment') is not None
    assert root.find('Notes') is not None


def test_generate_xml_min_values(
    test_schema_file_path: Path,
    test_patterns_file_path: Path,
    temp_xml_path: Path
) -> None:
    xml_generator: XmlGenerator = XmlGenerator(
        group_content_number_of_occurrences_getter=GroupContentRandomNumberOfOccurrencesGetter(unbounded_occurs=3),
        list_number_of_items_getter=ListMinNumberOfItemsGetter(),
        restriction_pattern_value_generator=JsonFileRestrictionPatternValueGenerator(test_patterns_file_path),
        restriction_value_generator=RestrictionMinValueGenerator(),
        force_default_value=False
    )
    assert_xml_result(xml_generator=xml_generator, xsd_path=test_schema_file_path, xml_path=temp_xml_path)
    root: Element = get_xml_root_element(temp_xml_path)
    items: Element | None = root.find('Items')
    assert items is not None
    if items is not None:
        prices: list[str] = [item.find('Price').text for item in items.findall('Item')]
        for price in prices:
            assert float(price) >= 0.00


def test_generate_xml_max_values(
    test_schema_file_path: Path,
    test_patterns_file_path: Path,
    temp_xml_path: Path
) -> None:
    xml_generator: XmlGenerator = XmlGenerator(
        group_content_number_of_occurrences_getter=GroupContentRandomNumberOfOccurrencesGetter(unbounded_occurs=3),
        list_number_of_items_getter=ListMaxNumberOfItemsGetter(unbounded_length=3),
        restriction_pattern_value_generator=JsonFileRestrictionPatternValueGenerator(test_patterns_file_path),
        restriction_value_generator=RestrictionMaxValueGenerator(),
        force_default_value=False
    )
    assert_xml_result(xml_generator=xml_generator, xsd_path=test_schema_file_path, xml_path=temp_xml_path)
    root: Element = get_xml_root_element(temp_xml_path)
    items: Element | None = root.find('Items')
    assert items is not None
    if items is not None:
        prices: list[str] = [item.find('Price').text for item in items.findall('Item')]
        for price in prices:
            assert float(price) <= 99999.99


def test_generate_xml_force_default(
    test_schema_file_path: Path,
    test_patterns_file_path: Path,
    temp_xml_path: Path
) -> None:
    xml_generator: XmlGenerator = XmlGenerator(
        group_content_number_of_occurrences_getter=GroupContentRandomNumberOfOccurrencesGetter(unbounded_occurs=3),
        list_number_of_items_getter=ListRandomNumberOfItemsGetter(unbounded_length=3),
        restriction_pattern_value_generator=JsonFileRestrictionPatternValueGenerator(test_patterns_file_path),
        restriction_value_generator=RestrictionRandomValueGenerator(),
        force_default_value=True
    )
    assert_xml_result(xml_generator=xml_generator, xsd_path=test_schema_file_path, xml_path=temp_xml_path)
    root: Element = get_xml_root_element(temp_xml_path)
    assert root.get('priority') == 'normal'
    items: Element | None = root.find('Items')
    assert items is not None
    if items is not None:
        for item in items.findall('Item'):
            assert item.get('available') == 'true'
