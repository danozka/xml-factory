import logging
import random
from logging import Logger

from xmlschema.validators import (
    XsdAtomicBuiltin,
    XsdFacet,
    XsdFractionDigitsFacet,
    XsdMaxExclusiveFacet,
    XsdMaxInclusiveFacet,
    XsdMaxLengthFacet,
    XsdMinExclusiveFacet,
    XsdMinInclusiveFacet,
    XsdMinLengthFacet,
    XsdPatternFacets,
    XsdSimpleType,
    XsdTotalDigitsFacet,
    XsdWhiteSpaceFacet
)

from xml_factory.domain.base_type import BaseType
from xml_factory.domain.restriction import Restriction
from xml_factory.domain.white_space_restriction import WhiteSpaceRestriction
from xml_factory.boolean_string_value_generator import BooleanStringValueGenerator
from xml_factory.date_string_value_generator import DateStringValueGenerator
from xml_factory.date_time_string_value_generator import DateTimeStringValueGenerator
from xml_factory.decimal_string_value_generator import DecimalStringValueGenerator
from xml_factory.hexadecimal_binary_string_value_generator import HexadecimalBinaryStringValueGenerator
from xml_factory.integer_string_value_generator import IntegerStringValueGenerator
from xml_factory.string_value_generator import StringValueGenerator
from xml_factory.time_string_value_generator import TimeStringValueGenerator


class XmlSimpleTypeValueGenerator:
    _log: Logger = logging.getLogger(__name__)
    _force_min_value: bool
    _force_max_value: bool
    _boolean_string_value_generator: BooleanStringValueGenerator
    _date_string_value_generator: DateStringValueGenerator
    _date_time_string_value_generator: DateTimeStringValueGenerator
    _decimal_string_value_generator: DecimalStringValueGenerator
    _hexadecimal_binary_string_value_generator: HexadecimalBinaryStringValueGenerator
    _integer_string_value_generator: IntegerStringValueGenerator
    _string_value_generator: StringValueGenerator
    _time_string_value_generator: TimeStringValueGenerator
    
    def __init__(
        self,
        force_min_value: bool = False,
        force_max_value: bool = False,
        boolean_string_value_generator: BooleanStringValueGenerator = BooleanStringValueGenerator(),
        date_string_value_generator: DateStringValueGenerator = DateStringValueGenerator(),
        date_time_string_value_generator: DateTimeStringValueGenerator = DateTimeStringValueGenerator(),
        decimal_string_value_generator: DecimalStringValueGenerator = DecimalStringValueGenerator(),
        hexadecimal_binary_string_value_generator: HexadecimalBinaryStringValueGenerator = (
            HexadecimalBinaryStringValueGenerator()
        ),
        integer_string_value_generator: IntegerStringValueGenerator = IntegerStringValueGenerator(),
        string_value_generator: StringValueGenerator = StringValueGenerator(),
        time_string_value_generator: TimeStringValueGenerator = TimeStringValueGenerator()
    ) -> None:
        self._force_min_value = force_min_value
        self._force_max_value = force_max_value
        self._boolean_string_value_generator = boolean_string_value_generator
        self._date_string_value_generator = date_string_value_generator
        self._date_time_string_value_generator = date_time_string_value_generator
        self._decimal_string_value_generator = decimal_string_value_generator
        self._hexadecimal_binary_string_value_generator = hexadecimal_binary_string_value_generator
        self._integer_string_value_generator = integer_string_value_generator
        self._string_value_generator = string_value_generator
        self._time_string_value_generator = time_string_value_generator

    def generate_xml_simple_type_value(self, xsd_simple_type: XsdSimpleType) -> str:
        if xsd_simple_type.is_list():
            raise NotImplementedError(f'List simple type {xsd_simple_type} not implemented')
        elif xsd_simple_type.is_union():
            raise NotImplementedError(f'Union simple type {xsd_simple_type} not implemented')
        else:
            restriction: Restriction = Restriction(
                name=xsd_simple_type.local_name,
                base_type=BaseType(
                    xsd_simple_type.local_name
                    if isinstance(xsd_simple_type, XsdAtomicBuiltin)
                    else xsd_simple_type.base_type.local_name
                ),
                enumeration=xsd_simple_type.enumeration
            )
            xmlschema_facet: XsdFacet
            for facet in xsd_simple_type.facets.values():
                if isinstance(facet, XsdFractionDigitsFacet):
                    restriction.fraction_digits = facet.value
                elif isinstance(facet, XsdMaxExclusiveFacet):
                    restriction.max_exclusive = float(facet.value)
                elif isinstance(facet, XsdMaxInclusiveFacet):
                    restriction.max_inclusive = float(facet.value)
                elif isinstance(facet, XsdMaxLengthFacet):
                    restriction.max_length = facet.value
                elif isinstance(facet, XsdMinExclusiveFacet):
                    restriction.min_exclusive = float(facet.value)
                elif isinstance(facet, XsdMinInclusiveFacet):
                    restriction.min_inclusive = float(facet.value)
                elif isinstance(facet, XsdMinLengthFacet):
                    restriction.min_length = int(facet.value)
                elif isinstance(facet, XsdPatternFacets):
                    restriction.pattern = facet.regexps[0]
                elif isinstance(facet, XsdTotalDigitsFacet):
                    restriction.total_digits = facet.value
                elif isinstance(facet, XsdWhiteSpaceFacet):
                    restriction.white_space = WhiteSpaceRestriction(facet.value)
            return self._get_restriction_value(restriction)

    def _get_restriction_value(self, restriction: Restriction) -> str:
        if restriction.enumeration is not None:
            return random.choice(restriction.enumeration)
        elif restriction.base_type == BaseType.time:
            return self._time_string_value_generator.generate_random_time_string_value()
        elif restriction.base_type == BaseType.boolean:
            return self._boolean_string_value_generator.generate_random_boolean_string_value()
        elif restriction.base_type == BaseType.date_time:
            return self._date_time_string_value_generator.generate_random_date_time_string_value()
        elif restriction.base_type == BaseType.date:
            return self._date_string_value_generator.generate_random_date_string_value()
        elif restriction.base_type == BaseType.string:
            if restriction.min_length and self._force_min_value and not restriction.pattern:
                return self._string_value_generator.generate_specific_length_string_value(
                    length=restriction.min_length,
                    white_space_restriction=restriction.white_space
                )
            elif restriction.max_length and self._force_max_value and not restriction.pattern:
                return self._string_value_generator.generate_specific_length_string_value(
                    length=restriction.max_length,
                    white_space_restriction=restriction.white_space
                )
            else:
                return self._string_value_generator.generate_random_string_value(restriction)
        elif restriction.base_type == BaseType.integer:
            if restriction.min_inclusive and self._force_min_value:
                return str(int(restriction.min_inclusive))
            elif restriction.max_inclusive and self._force_max_value:
                return str(int(restriction.max_inclusive))
            else:
                return self._integer_string_value_generator.generate_random_integer_string_value(restriction)
        elif restriction.base_type == BaseType.decimal:
            if restriction.min_inclusive and self._force_min_value:
                return self._decimal_string_value_generator.generate_decimal_string_value(
                    value=restriction.min_inclusive,
                    fraction_digits=restriction.fraction_digits
                )
            elif restriction.max_inclusive and self._force_max_value:
                return self._decimal_string_value_generator.generate_decimal_string_value(
                    value=restriction.max_inclusive,
                    fraction_digits=restriction.fraction_digits
                )
            else:
                return self._decimal_string_value_generator.generate_random_decimal_string_value(restriction)
        elif restriction.base_type == BaseType.hex_binary:
            if restriction.min_length and self._force_min_value:
                return self._hexadecimal_binary_string_value_generator.generate_specific_length_hexadecimal_binary_string_value(
                    restriction.min_length
                )
            elif restriction.max_length and self._force_max_value:
                return self._hexadecimal_binary_string_value_generator.generate_specific_length_hexadecimal_binary_string_value(
                    restriction.max_length
                )
            else:
                return self._hexadecimal_binary_string_value_generator.generate_random_hexadecimal_binary_string_value(
                    restriction
                )
        else:
            raise NotImplementedError(f'Unsupported restriction base type \'{restriction.base_type}\'')
