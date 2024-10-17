import pytest

from plaster_yaml.loader import resolve_use


@pytest.mark.parametrize("name", ["app1", "app2"])
def test_resolve_app_factory(name):
    main = resolve_use(f"egg:{name}#main", "paste.app_factory")
    assert main(None) == name


def test_resolve_app_factory_unexisting():
    with pytest.raises(ValueError) as ctx:
        resolve_use("egg:ivenoideawhatiamdoing#main", "paste.app_factory")
    assert (
        str(ctx.value)
        == "Entrypoint paste.app_factory is missing for egg:ivenoideawhatiamdoing#main"
    )
