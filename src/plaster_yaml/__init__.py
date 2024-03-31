from .loader import Loader
from .compat import importlib_metadata

__all__ = ["Loader"]
__version__ = importlib_metadata.version("plaster-yaml")
