# plaster-yaml

## Introduction

Configure your applications with YAML structured data.

The `plaster-yaml` plugin lets applications, notably [Pyramid](
https://trypyramid.com) applications but also other applications that
use the [plaster](
https://docs.pylonsproject.org/projects/plaster/en/latest/) loader
interface, accept YAML configuration sources.

By default, Pyramid (etc.) uses the PasteDeploy (.ini) file format for
its configuration.  With the `plaster-yaml` plugin, Pyramid
applications can instead be configured with a YAML configuration file.

For example:

```
pserve development.yaml
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

The `plaster-yaml` plugin must be "registered".  This is done by
configuring a Python package "entry point" using the packaging tool of
your choice.  How this is done depends on the packaging tool.
Examples are given below.

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
