import sys
from pathlib import Path

import pytest
from plaster import PlasterURL, parse_uri

from plaster_yaml import Loader


@pytest.fixture(scope="session", autouse=True)
def root() -> Path:
    return Path(__file__).parent.absolute()


@pytest.fixture(scope="session", autouse=True)
def uri(root) -> PlasterURL:
    cfg = root / "config.yaml"
    return parse_uri(f"file+yaml://{cfg}")


@pytest.fixture
def loader(uri):
    yield Loader(uri)


@pytest.fixture(scope="session", autouse=True)
def fake_packages(root: Path) -> None:
    fake_packages = root / "dummy_packages"
    for dirs in fake_packages.iterdir():
        sys.path.insert(0, str(dirs))
