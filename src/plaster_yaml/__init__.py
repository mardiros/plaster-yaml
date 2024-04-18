from .compat import importlib_metadata
from .loader import Loader

__all__ = ["Loader"]
__version__ = importlib_metadata.version("plaster-yaml")
