import pathlib
from unittest.mock import call, patch

import pytest
from gunicorn.app.pasterapp import serve as gunicorn_serve_paste
from waitress import serve_paste as waitress_serve_paste

from plaster_yaml.loader import resolve_use

here = str(pathlib.Path(__file__).parent.absolute())


def test_resolve_waitress():
    main = resolve_use("egg:waitress#main", "paste.server_runner")
    assert main == waitress_serve_paste


def test_resolve_gunicorn():
    main = resolve_use("egg:gunicorn#main", "paste.server_runner")
    assert main == gunicorn_serve_paste


@pytest.mark.usefixtures("loader")
def test_defaults(loader):
    assert loader.defaults == {
        "__file__": f"{here}/config.yaml",
        "here": here,
    }


@pytest.mark.usefixtures("loader")
def test_get_sections(loader):
    assert loader.get_sections() == ["app", "server", "logging"]


@pytest.mark.usefixtures("loader")
def test_get_settings(loader):
    settings = loader.get_settings(section="app")
    assert settings == {
        "dummy_path": f"{here}/dummy_file.yaml",
        "pyramid.debug_authorization": False,
        "pyramid.debug_notfound": False,
        "pyramid.debug_routematch": False,
        "pyramid.default_locale_name": "en",
        "pyramid.includes": [],
        "pyramid.reload_templates": False,
        "use": "egg:pyramid_helloworld",
    }

@pytest.mark.usefixtures("loader")
def test_get_wsgi_app_settings(loader):
    settings = loader.get_wsgi_app_settings()
    assert settings == {
        "dummy_path": f"{here}/dummy_file.yaml",
        "pyramid.debug_authorization": False,
        "pyramid.debug_notfound": False,
        "pyramid.debug_routematch": False,
        "pyramid.default_locale_name": "en",
        "pyramid.includes": [],
        "pyramid.reload_templates": False,
        "use": "egg:pyramid_helloworld",
    }


@patch("plaster_yaml.loader.dictConfig")
@pytest.mark.usefixtures("loader")
def test_setup_logging(dictConfig, loader):
    loader.setup_logging(None)
    assert dictConfig.call_args_list == [call(loader._conf["logging"])]


@patch("waitress.serve_paste")
@pytest.mark.usefixtures("loader")
def test_get_wsgi_server(serve_paste, loader):
    wsgi_server = loader.get_wsgi_server()
    assert serve_paste.call_args_list == []
    app = object()
    wsgi_server(app)
    assert serve_paste.call_args_list == [
        call(
            app,
            loader.defaults,
            host="0.0.0.0",
            port=8000,
        )
    ]


@pytest.mark.usefixtures("loader")
def test_get_wsgi_app(loader):
    wsgi_app = loader.get_wsgi_app()
    assert wsgi_app.registry.settings["dummy_path"] == f"{here}/dummy_file.yaml"

    http_start_response = {}

    def start_response(status, headers):
        http_start_response["status"] = status
        http_start_response["headers"] = headers

    resp = wsgi_app({"REQUEST_METHOD": "GET"}, start_response)
    assert resp == [b"Hello World!"]
    assert http_start_response == {
        "headers": [
            ("Content-Type", "text/html; charset=UTF-8"),
            ("Content-Length", "12"),
        ],
        "status": "200 OK",
    }
