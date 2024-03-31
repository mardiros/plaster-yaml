# plaster-yaml

Configure your applications with YAML (and JSON) structured data.

[![codecov](https://codecov.io/gh/mardiros/plaster-yaml/graph/badge.svg?token=LKGPH2OJDN)](https://codecov.io/gh/mardiros/plaster-yaml)

## Introduction

The `plaster-yaml` plugin lets applications, notably [Pyramid](
https://trypyramid.com) applications but also other applications that
use the [plaster](
https://docs.pylonsproject.org/projects/plaster/en/latest/) loader
interface, accept YAML configuration sources.

By default, Pyramid (etc.) uses the PasteDeploy (.ini) file format for
its configuration.  With the `plaster-yaml` plugin, Pyramid
applications can also be configured with a YAML configuration file.

For example, one application can be run either of these ways:

```
pserve development.yaml
pserve development.ini
```

Because JSON is a subset of YAML `plaster-yaml` also supports JSON
configuration files.  The "With `pyproject.toml` and a `setuptools`
`build` back-end" section below contains a JSON example.

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

The `plaster-yaml` plugin must be "registered".  This is done by
configuring a Python package "entry point" using the packaging tool of
your choice.  How this is done depends on the packaging tool.
Examples are given below.

It is the entry point's name, as will be clear in the examples, that
"connects" the filename extension of a configuration file to the
loader able to parse it.  While it is not necessary to know the
details, here are the basic concepts: The entry point's name is a
[config_uri](
https://docs.pylonsproject.org/projects/plaster/en/latest/glossary.html#term-config-uri).
The scheme is that part of the URI to the left of the colon, and is
itself divisible.  One of the scheme's components is matched with the
filename extension to select the correct loader.

When developing, using an [editable](
https://setuptools.pypa.io/en/latest/userguide/development_mode.html)
install that executes your unpackaged code, after changing your
package's configuration your packaging tool must be run in order to
finalize the registration.  Examples are given below.

No special steps must be taken after configuring a entry point and
(correctly) packaging your project.  The `plaster-yaml` plugin is
registered when your project's package is installed.

NOTE:\
All of the examples given below show not only how the one entry point
required to use `plaster-yaml` is configured, but also show how to
configure the entry point that makes your application into a WSGI,
web-based, application.  The WSGI entry point is always required for
Pyramid web applications.

## With poetry

Plugin registration is configured in your `pyproject.toml`, as
follows:

```
[tool.poetry.plugins."paste.app_factory"]
main = "<PATH_TO_MODULE_CONTAINING_MAIN>:main"

[tool.poetry.plugins."plaster.loader_factory"]
"file+yaml" = "plaster_yaml:Loader"
```

When developing, run `poetry install` to register your plugin after
adding the above to your `pyproject.toml`.

## With setuptools

When developing, run `pip install -e .` to register your plugin after
using either of approaches below.

### With `pyproject.toml` and a `setuptools` `build` back-end

This is the preferred method.

Plugin registration may be configured in your `pyproject.toml`, as
follows:

```
[project.entry-points.'paste.app_factory']
main = '<my_app>:main']

[project.entry-points.'plaster.loader_factory']
'file+yaml' = 'plaster_yaml:Loader'
```

Adding a final line to the example lets the application support JSON
in additional to YAML and .ini config files:

```
[project.entry-points.'paste.app_factory']
main = '<my_app>:main']

[project.entry-points.'plaster.loader_factory']
'file+yaml' = 'plaster_yaml:Loader'
'file+json' = 'plaster_yaml:Loader'
```

### With `setup.py`

This method is generally obsolete, but it can be used when the
`[project.entry-points]` table is declared "dynamic".  However, this
method must be used when the deprecated `python setup.py ...`
command is the package building method.

Plugin registration may be configured in your `setup.py`, as
follows:

```
setup(
    ...,
    entry_points={
     'paste.app_factory': ['main = <my_app>:main'],
     'plaster.loader_factory': ['file+yaml = plaster_yaml:Loader'],
     ...
    },
)
```

## Troubleshooting

The following exception means that you did not successfully register
the `plaster-yaml` plugin:

```
plaster.exceptions.LoaderNotFound: Could not find a matching loader for the scheme "file+yaml", protocol "wsgi".
```

Read the relevant "Usage" sub-section, above, to find out how to
register it properly.

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
  disable_existing_loggers: False
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
