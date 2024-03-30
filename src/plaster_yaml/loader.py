"""Implement a loader for plaster using yaml format."""
import pathlib
from logging.config import dictConfig
from typing import Callable

import sys

if sys.version_info < (3, 10):
    import importlib_metadata

    class importlib:
        pass

    setattr(importlib, "metadata", importlib_metadata)
else:
    import importlib.metadata

import plaster
import yaml

DEFAULT_LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "console": {
            "format": "%(asctime)s [%(levelname)s]: %(name)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "stream": "ext://sys.stderr",
            "formatter": "console",
        },
    },
    "root": {"level": "ERROR", "handlers": ["console"]},
}


def resolve_use(use: str, entrypoint: str) -> Callable:
    try:
        pkg, name = use.split("#")
    except ValueError:
        pkg, name = use, "main"
    try:
        scheme, pkg = pkg.split(":")
    except ValueError:
        scheme = "egg"
    if scheme != "egg":
        raise ValueError(f"{use}: unsupported scheme {scheme}")

    eps = importlib.metadata.entry_points(group=entrypoint, name=name)
    (runner,) = [ep for ep in eps if ep.module == pkg]
    return runner.load()


class Loader(plaster.ILoader):
    def __init__(self, uri):
        self.uri = uri

        path = pathlib.Path(self.uri.path)
        self.defaults = {
            "__file__": str(path.absolute()),
            "here": str(path.parent),
        }
        with open(self.uri.path, "r") as stream:
            self._conf = yaml.safe_load(stream)

    def get_sections(self):
        return ["app"]

    def get_settings(self, section=None, defaults=None):
        # fallback to the fragment from config_uri if no section is given
        if not section:
            section = self.uri.fragment or "app"
        # if section is still none we could fallback to some
        # loader-specific default

        result = self.defaults.copy()
        if defaults is not None:
            result.update(defaults)

        settings = self._conf[section].copy()

        for key, val in settings.items():
            if isinstance(val, str):
                if "%(here)s" in val:
                    settings[key] = val % self.defaults
        return settings

    def get_wsgi_app_settings(self, name=None, defaults=None):
        return self.get_settings(name, defaults)

    def setup_logging(self, config_vars):
        dictConfig(self._conf.get("logging", DEFAULT_LOGGING_CONFIG))

    def get_wsgi_server(self, name=None, defaults=None):
        settings = self.get_settings("server", defaults)
        server = resolve_use(settings.pop("use"), "paste.server_runner")
        return lambda app: server(app, self.defaults, **settings)

    def get_wsgi_app(self, name=None, defaults=None):
        settings = self.get_settings(name, defaults)
        use = resolve_use(settings.pop("use"), "paste.app_factory")
        return use(defaults, **settings)
