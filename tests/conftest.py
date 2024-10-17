from pathlib import Path
import sys

import pytest
from plaster import parse_uri

from plaster_yaml import Loader

cfg = Path(__file__).parent / "config.yaml"
uri = parse_uri(f"file+yaml://{cfg}")


@pytest.fixture
def loader():
    yield Loader(uri)


@pytest.fixture(scope="session", autouse=True)
def root() -> Path:
    return Path(__file__).parent.absolute()


@pytest.fixture(scope="session", autouse=True)
def fake_packages(root: Path) -> None:
    fake_packages = root / "dummy_packages"
    for dirs in fake_packages.iterdir():
        sys.path.insert(0, str(dirs))
