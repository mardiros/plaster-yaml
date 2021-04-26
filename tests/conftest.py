import pathlib

import pytest
from plaster import parse_uri

from plaster_yaml import Loader

cfg = pathlib.Path(__file__).parent / "config.yaml"
uri = parse_uri(f"file+yaml://{cfg}")


@pytest.fixture
def loader():
    yield Loader(uri)
