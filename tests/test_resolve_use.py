import pytest

from plaster_yaml.loader import resolve_use


@pytest.mark.parametrize("name", ["app1", "app2"])
def test_resolve_app_factory(name):
    main = resolve_use(f"egg:{name}#main", "paste.app_factory")
    assert main(None) == name


@pytest.mark.parametrize(
    "import_name,name",
    [
        ("myns.app1", "myns.app2"),
        ("myns.app2", "myns.app2"),
        ("myns-app1", "myns.app1"),
        ("myns_app1", "myns.app1"),
        ("Myns_App1", "myns.app1"),
    ],
)
def test_resolve_app_factory_namespace_packages(import_name, name):
    main = resolve_use(f"egg:{name}#main", "paste.app_factory")
    assert main(None) == name


def test_resolve_app_factory_unexisting():
    with pytest.raises(ValueError) as ctx:
        resolve_use("egg:ivenoideawhatiamdoing#main", "paste.app_factory")
    assert (
        str(ctx.value)
        == "Entrypoint paste.app_factory is missing for egg:ivenoideawhatiamdoing#main"
    )
