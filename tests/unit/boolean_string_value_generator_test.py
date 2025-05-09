from xml_factory.simple.boolean_string_value_generator import BooleanStringValueGenerator


def test_generate_random_boolean_string_value() -> None:
    boolean_string_value_generator: BooleanStringValueGenerator = BooleanStringValueGenerator()
    results = set()
    for _ in range(100):
        results.add(boolean_string_value_generator.generate_random_boolean_string_value())
    assert len(results) == 2
    assert results == {'true', 'false'}
