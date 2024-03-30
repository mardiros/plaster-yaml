# Plaster Yaml

## Introduction

By default, Pyramid uses a PasteDeploy (.ini) file format for its
configuration.

When the ``plaster-yaml`` a plugin is used, Pyramid applications are
instead configured with a YAML configuration file.

e.g.

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

## With poetry

The plugin is registered in your `pyproject.toml, as follows`:


```
[tool.poetry.plugins."paste.app_factory"]
main = "<PATH_TO_MODULE_CONTAINING_MAIN>:main"

[tool.poetry.plugins."plaster.loader_factory"]
"file+yaml" = "plaster_yaml:Loader"
```

When developing, using an "editable" install that executes your
unpackaged code, `poetry install` must be run to finalize the
registration.

## With setuptools

```
setup(
    ...,
    entry_points={
     'paste.app_factory': ['main = <my_app>:main'],
     'plaster.loader_factory': ['yaml = plaster_yaml:Loader'],
     ...
    },
)
```

When developing, using an "editable" install that executes your
unpackaged code, `pip install -e .` must be run to finalize the
registration.

## Troubleshooting

The following exception means that you did not register the plugin:

```
plaster.exceptions.LoaderNotFound: Could not find a matching loader for the scheme "file+yaml", protocol "wsgi".
```

Read the relevant "Usage" sub-section, above, to find out how to
register it properly.
