# plaster-yaml

Configure your applications with YAML (and JSON) structured data.

[![CI](https://github.com/mardiros/plaster-yaml/actions/workflows/main.yml/badge.svg)](https://github.com/mardiros/plaster-yaml/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/mardiros/plaster-yaml/graph/badge.svg?token=LKGPH2OJDN)](https://codecov.io/gh/mardiros/plaster-yaml)

## Introduction

The `plaster-yaml` plugin lets applications, notably [Pyramid](
https://trypyramid.com) applications but also other applications that
use the [plaster](
https://docs.pylonsproject.org/projects/plaster/en/latest/) loader
interface, accept YAML configuration sources.

By default, Pyramid (etc.) uses the PasteDeploy (.ini) file format for
its configuration. PasteDeploy has become obsolete and has been replace
by [plaster](https://docs.pylonsproject.org/projects/plaster/) and accept
plugins to write more file format.

With the `plaster-yaml` plugin, Pyramid
applications can also be configured with a YAML configuration file.

For example, one application can be run either of these ways:

Because JSON is a subset of YAML `plaster-yaml` also supports JSON
configuration files.  The "With `pyproject.toml` and a `setuptools`
`build` back-end" section below contains a JSON example.

```bash
pserve development.yaml
pserve development.json
pserve development.ini
```

## Installation

## With poetry

```
poetry add plaster-yaml
```

## With pip

```
pip install plaster-yaml
```

## Usage

WSGI application that use plaster have to register an [entry point](https://packaging.python.org/en/latest/specifications/entry-points/),
from a ``paste.app_factory``.

## With poetry

App registration is configured in your `pyproject.toml`, as
follows:

```
[tool.poetry.plugins."paste.app_factory"]
main = "<PATH_TO_MODULE_CONTAINING_MAIN>:main"

```

When developing, run `poetry install` to register your application after
adding the above to your `pyproject.toml`.

## With setuptools

When developing, run `pip install -e .` to register your application after
using either of approaches below.

### With `pyproject.toml` and a `setuptools` `build` back-end

This is the preferred method.

Plugin registration may be configured in your `pyproject.toml`, as
follows:

```
[project.entry-points.'paste.app_factory']
main = '<my_app>:main']
```

Adding a final line to the example lets the application support JSON
in additional to YAML and .ini config files:

```
[project.entry-points.'paste.app_factory']
main = '<my_app>:main']
```

### With `setup.py`

This method is generally obsolete, but it can be used when the
`[project.entry-points]` table is declared "dynamic".  However, this
method must be used when the deprecated `python setup.py ...`
command is the package building method.

Application registration may be configured in your `setup.py`, as
follows:

```
setup(
    ...,
    entry_points={
     'paste.app_factory': ['main = <my_app>:main'],
     ...
    },
)
```

## Appendix: A sample YAML config file for Pyramid

The sample YAML config file shown here configures the MYAPP Pyramid
application.  The YAML mapping of the `app` key is presented to the
Pyramid application as a Python dictionary.  (Excepting the "use" key,
which is where the system is told that the "MYAPP" python package is
the one to use.)

Within your [view callable](
https://docs.pylonsproject.org/projects/pyramid/en/2.0-branch/glossary.html#term-view-callable)
code, the code which processes a web request and produces a response
for rendering, the "my_config_data" configuration value is available
via `request.registry.settings["my_config_data"]`.  That is, if the
usual coding idiom is used and your view is defined with `def
myview(request):`.

Likewise, the settings dict is available to your configuration code as
`settings`.  Again, assuming the usual coding idiom of `def
main(global_config, **settings):` is used in your `__init__.py`.  The
`global_config` variable is then a dict containing the content of the
config file's top-level `DEFAULT` key, if any.

For more information see: [the Pyramid Startup documentation](
https://docs.pylonsproject.org/projects/pyramid/en/latest/narr/startup.html)

```
###
# app configuration
# http://docs.pylonsproject.org/projects/pyramid/en/latest/narr/environment.html
###

app:
  "use": "egg:MYAPP"

  "pyramid.reload_templates": false
  "pyramid.debug_authorization": false
  "pyramid.debug_notfound": false
  "pyramid.debug_routematch": false
  "pyramid.default_locale_name": en
  "pyramid.includes": []

  "my_config_data": "Fe Fi Fo Fum"

DEFAULT:
  some_data_which_assists_app_startup: {automatic: false}

server:
  use: egg:waitress#main
  host: 0.0.0.0
  port: 6543

logging:
  version: 1
  disable_existing_loggers: false
  formatters:
    console:
      format: '%(asctime)s [%(levelname)s]: %(name)s - %(message)s'
  handlers:
    console:
      class: logging.StreamHandler
      level: INFO
      stream: ext://sys.stdout
      formatter: console
  root:
    level: INFO
    handlers:
      - console
  loggers:
    dummy:
      level: DEBUG
```
