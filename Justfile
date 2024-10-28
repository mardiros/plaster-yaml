package := 'plaster_yaml'
default_unittest_suite := 'tests'

install:
    uv sync --group dev --group uwsgi

lint:
    uv run ruff check .

test: lint unittest

unittest test_suite=default_unittest_suite:
    uv run pytest -sxv {{test_suite}}

#[doc("write eggs for testing")]
write_eggs:
    #!/bin/bash
    for app in tests/dummy_packages/*; do
        pushd . > /dev/null
        cd $app && python setup.py egg_info
        popd > /dev/null
    done

lf:
    uv run pytest -sxvvv --lf

cov test_suite=default_unittest_suite:
    rm -f .coverage
    rm -rf htmlcov
    uv run pytest --cov-report=html --cov={{package}} {{test_suite}}
    xdg-open htmlcov/index.html

fmt:
    uv run ruff check --fix .
    uv run ruff format src tests

mypy:
    uv run mypy src/ tests/


release major_minor_patch: test && changelog
    uvx pdm bump {{major_minor_patch}}
    uv sync

changelog:
    uv run python scripts/write_changelog.py
    cat CHANGELOG.md >> CHANGELOG.md.new
    rm CHANGELOG.md
    mv CHANGELOG.md.new CHANGELOG.md
    $EDITOR CHANGELOG.md

publish:
    git commit -am "Release $(uv run scripts/get_version.py)"
    poetry build
    poetry publish
    git push
    git tag "v$(uv run scripts/get_version.py)"
    git push origin "v$(uv run scripts/get_version.py)"
