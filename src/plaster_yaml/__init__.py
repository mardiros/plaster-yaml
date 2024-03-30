import sys

if sys.version_info < (3, 10):
    import importlib_metadata

    class importlib:
        pass

    setattr(importlib, "metadata", importlib_metadata)
else:
    import importlib.metadata

from .loader import Loader  # noqa

__version__ = importlib.metadata.version("plaster-yaml")
