import sys

if sys.version_info >= (3, 10):
    from importlib import metadata as importlib_metadata
else:
    import importlib_metadata

__all__ = ["importlib_metadata"]
