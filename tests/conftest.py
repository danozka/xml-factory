import logging
import pkgutil
from pathlib import Path


logging.basicConfig(
    format='%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
    level=logging.DEBUG
)
fixtures_directory_name: str = 'fixtures'
fixtures_directory_path: Path = Path(__file__).parent.joinpath(fixtures_directory_name)
pytest_plugins: list[str] = [
    f'{fixtures_directory_name}.{module}' for _, module, _ in pkgutil.iter_modules([str(fixtures_directory_path)])
]
