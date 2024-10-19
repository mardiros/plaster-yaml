## 2.0.0  -  2024-10-19

* /!\BREAKING CHANGE Restore the autoregistrion of the plaster-yaml file format in plaster.

You don't need to register the plaster-yaml entrypoint for file format .yaml, .yml and .json

Remove the entrypoint registered in your package for the migration

Fix for poetry, application that use plater-yaml registered the plugin with
those lines, remove them to avoid the conflict.

```
[tool.poetry.plugins."plaster.loader_factory"]
"file+yaml" = "plaster_yaml:Loader"
```

## 1.1.3  -  2024-10-19

* Revert register the plaster yaml entrypoints directly, fixing a breaking change

## 1.1.2  -  2024-10-19

* Also fix non namespace packaging container underscores

## 1.1.1  -  2024-10-17

* Add an experimental feature to get it working with uwsgi

## 1.1.0  -  2024-10-17

* Register the plaster yaml entrypoints directly, the app does not need to register it
* Fix supports for namespace package
* Add supports for python 3.12 ( CI )

## 1.0.2  -  2024-04-18

* Fix the get_settings() section, now the app may be named as your convenience
* Remove compativility with 3.8.0, starting at 3.8.1

## Version 1.0.1 - 2024-04-01

* Fix python 3.8 and 3.9 usage by using importlib_metadata
* Improve the readme file.

## Version 1.0.0 - 2024-03-30

* Remove pkg_resources in favor has importlib.metadata
* Remove python 3.7 support

## Version 0.2.0 - 2021-05-02

* Implementation get_wsgi_app_settings for the Loader

## Version 0.1.1 - 2021-04-26

* Fix default logging

## Version 0.1.0 - 2021-04-26

* Initial Release
