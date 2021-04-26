# Plaster Yaml

## Introduction

By default, Pyramid use a paste format file to loads its configuration,

here is a plugin to use a yaml file instead to configure your pyramid
application.

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

You need to register this plugin in your `pyproject.toml`:


```
[tool.poetry.plugins."paste.app_factory"]
main = "<PATH_TO_MODULE_CONTAINING_MAIN>:main"

[tool.poetry.plugins."plaster.loader_factory"]
"file+yaml" = "plaster_yaml:Loader"
```

You must run `poetry install` to finalize the registration.

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

You must run `pip install -e .` to finallize the registration.

## Troubleshouting

If you get the following exception:

```
plaster.exceptions.LoaderNotFound: Could not find a matching loader for the scheme "file+yaml", protocol "wsgi".
```

It meast that you did not register the pluging. Read the usage section
for to register it properly.

