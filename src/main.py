import logging
import sys
from pathlib import Path

import typer
from typing_extensions import Annotated

from xml_generator import XmlGenerator


def main(
    xsd: Annotated[Path, typer.Option(help='XSD file path', show_default=False)],
    xml: Annotated[Path, typer.Option(help='Output XML path', show_default=False)],
    root: Annotated[str, typer.Option(help='Name of the XSD root element', show_default=False)],
    log_level: Annotated[
        str,
        typer.Option(help='Application logging level: DEBUG, INFO, WARNING, ERROR or CRITICAL')
    ] = 'INFO',
    force_min_occurs: Annotated[
        bool,
        typer.Option(default='--force-min-occurs', help='Force minimum occurrence on each element')
    ] = False,
    force_max_occurs: Annotated[
        bool,
        typer.Option(default='--force-max-occurs', help='Force maximum occurrence on each element')
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
    xml_generator: XmlGenerator = XmlGenerator(
        force_min_occurs,
        force_max_occurs,
        force_default_value,
        force_min_value,
        force_max_value
    )
    exit_code: int = xml_generator.generate_xml(xsd_path=xsd, xml_path=xml, root_element_name=root)
    sys.exit(exit_code)


if __name__ == '__main__':
    typer.run(main)
