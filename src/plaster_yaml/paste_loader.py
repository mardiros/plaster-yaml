"""
And experimental module to load yaml file using paste.deploy (patched)

The paste.deploy patch: https://github.com/Pylons/pastedeploy/pull/46/files
"""

from logging.config import dictConfig
from pathlib import Path

try:
    from paste.deploy.loadwsgi import (
        LoaderContext,
        _Loader,  # type: ignore
        loadcontext,
    )
except ImportError:

    class _Loader:
        def absolute_name(self, name): ...

    class LoaderContext:
        def __init__(self, *args, **kwargs): ...

    def loadcontext(*args, **kwargs): ...


import yaml


class YamlPasteDeployLoader(_Loader):
    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.defaults = {
            "here": str(self.filepath.absolute()),
        }
        with self.filepath.open("r") as stream:
            self._conf = yaml.safe_load(stream)

    def find_config_section(self, object_type, name):
        section = conf = None
        for name_options in object_type.config_prefixes:
            for name_prefix in name_options:
                if f"{name_prefix}:{name}" in self._conf:
                    section = f"{name_prefix}:{name}"
                    conf = self._conf[section]
                    break
                if name == "main":
                    if name_prefix in self._conf:
                        section = name_prefix
                        conf = self._conf[name_prefix]
                        break
        return section, conf

    def _context_from_use(self, object_type, local_conf, global_conf, section):
        use = local_conf.pop("use")
        context = self.get_context(object_type, name=use, global_conf=global_conf)
        context.local_conf.update(local_conf)
        context.loader = self
        if context.protocol is None:
            # Determine protocol from section type
            section_protocol = section.split(":", 1)[0]
            if section_protocol in ("application", "app"):
                context.protocol = "paste.app_factory"
            elif section_protocol in ("composit", "composite"):
                context.protocol = "paste.composit_factory"
            else:
                # This will work with 'server' and 'filter', otherwise it
                # could fail but there is an error message already for
                # bad protocols
                context.protocol = "paste.%s_factory" % section_protocol
        return context

    def get_context(self, object_type, name=None, global_conf=None):
        if self.absolute_name(name):
            return loadcontext(
                object_type,
                name,
                relative_to=str(self.filepath.parent),
                global_conf=global_conf,
            )

        section, local_conf = self.find_config_section(object_type, name=name)
        if not local_conf:
            raise ValueError(f"Missing {name}")
        if "use" not in local_conf:
            raise ValueError(f"Missing use in {section} of {name}")
        context = self._context_from_use(object_type, local_conf, global_conf, section)
        return context

    def setup_logging(self) -> None:
        if "logging" in self._conf:
            dictConfig(self._conf["logging"])


def load_yaml(object_type, uri, path: str, name, relative_to, global_conf):
    pathobj = Path(path)
    if not pathobj.is_file():
        raise ValueError(f"File expected: {path}")
    loader = YamlPasteDeployLoader(pathobj)
    loader.setup_logging()
    return loader.get_context(object_type, name, global_conf)
