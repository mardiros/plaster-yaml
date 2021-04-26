import pkg_resources

from .loader import Loader  # noqa

__version__ = pkg_resources.get_distribution("plaster-yaml").version
