import logging
import sys
from pathlib import Path

import typer
from typing_extensions import Annotated

from xml_factory import (
    GroupContentAtLeastOneNumberOfOccurrencesGetter,
    GroupContentMaxNumberOfOccurrencesGetter,
    GroupContentMinNumberOfOccurrencesGetter,
    GroupContentRandomNumberOfOccurrencesGetter,
    IGroupContentNumberOfOccurrencesGetter,
    XmlGenerator,
    XmlSimpleTypeValueGenerator
)


def main(
    xsd: Annotated[Path, typer.Option(help='XSD file path', show_default=False)],
    xml: Annotated[Path, typer.Option(help='Output XML path', show_default=False)],
    root: Annotated[str, typer.Option(help='Name of the XSD root element', show_default=False)],
    log_level: Annotated[
        str,
        typer.Option(help='Application logging level: DEBUG, INFO, WARNING, ERROR or CRITICAL')
    ] = 'INFO',
    unbounded_occurs: Annotated[
        int,
        typer.Option(default='--unbounded-occurs', help='Number of occurrences for unbounded components')
    ] = 5,
    force_min_occurs: Annotated[
        bool,
        typer.Option(default='--force-min-occurs', help='Force minimum occurrence on each component')
    ] = False,
    force_max_occurs: Annotated[
        bool,
        typer.Option(default='--force-max-occurs', help='Force maximum occurrence on each component')
    ] = False,
    force_at_least_one_occurs: Annotated[
        bool,
        typer.Option(
            default='--force-at-least-one-occurs',
            help='Force at least one occurrence for optional components'
        )
    ] = False,
    force_default_value: Annotated[
        bool,
        typer.Option(default='--force-default', help='Force default value on each element')
    ] = False,
    force_min_value: Annotated[
        bool,
        typer.Option(default='--force-min', help='Force minimum value on each element')
    ] = False,
    force_max_value: Annotated[
        bool,
        typer.Option(default='--force-max', help='Force maximum value on each element')
    ] = False
) -> None:
    logging.basicConfig(
        format='%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s',
        datefmt='%d-%m-%Y %H:%M:%S',
        level=log_level
    )
    active_options: int = sum([force_min_occurs, force_max_occurs, force_at_least_one_occurs])
    if active_options > 1:
        logging.error(
            'Only one of \'--force-min-occurs\', \'--force-max-occurs\', or \'--force-at-least-one-occurs\' '
            'can be set to True'
        )
        sys.exit(1)
    group_content_number_of_occurrences_getter: IGroupContentNumberOfOccurrencesGetter
    if force_min_occurs:
        group_content_number_of_occurrences_getter = GroupContentMinNumberOfOccurrencesGetter()
    elif force_max_occurs:
        group_content_number_of_occurrences_getter = GroupContentMaxNumberOfOccurrencesGetter(unbounded_occurs)
    elif force_at_least_one_occurs:
        group_content_number_of_occurrences_getter = GroupContentAtLeastOneNumberOfOccurrencesGetter()
    else:
        group_content_number_of_occurrences_getter = GroupContentRandomNumberOfOccurrencesGetter(unbounded_occurs)
    xml_factory: XmlGenerator = XmlGenerator(
        group_content_number_of_occurrences_getter=group_content_number_of_occurrences_getter,
        force_default_value=force_default_value,
        xml_simple_type_value_generator=XmlSimpleTypeValueGenerator(
            force_min_value=force_min_value,
            force_max_value=force_max_value
        )
    )
    exit_code: int = xml_factory.generate_xml(xsd_path=xsd, xml_path=xml, root_element_name=root)
    sys.exit(exit_code)


if __name__ == '__main__':
    typer.run(main)
