from importlib import metadata

from .loader import Loader

__all__ = ["Loader"]
__version__ = metadata.version("plaster-yaml")
