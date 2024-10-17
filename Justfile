package := 'plaster_yaml'
default_unittest_suite := 'tests'

install:
    poetry install --with dev

lint:
    poetry run flake8 && echo "$(tput setaf 10)Success: no lint issue$(tput setaf 7)"

test: lint unittest

unittest test_suite=default_unittest_suite:
    poetry run pytest -sxv {{test_suite}}

#[doc("write eggs for testing")]
write_eggs:
    #!/bin/bash
    for app in tests/dummy_packages/*; do
        pushd . > /dev/null
        cd $app && python setup.py egg_info
        popd > /dev/null
    done

lf:
    poetry run pytest -sxvvv --lf

cov test_suite=default_unittest_suite:
    rm -f .coverage
    rm -rf htmlcov
    poetry run pytest --cov-report=html --cov={{package}} {{test_suite}}
    xdg-open htmlcov/index.html


black:
    poetry run isort .
    poetry run black .


release major_minor_patch: test && changelog
    poetry version {{major_minor_patch}}
    poetry install

changelog:
    poetry run python scripts/write_changelog.py
    cat CHANGELOG.md >> CHANGELOG.md.new
    rm CHANGELOG.md
    mv CHANGELOG.md.new CHANGELOG.md
    $EDITOR CHANGELOG.md

publish:
    git commit -am "Release $(poetry version -s)"
    poetry build
    poetry publish
    git push
    git tag "$(poetry version -s)"
    git push origin "$(poetry version -s)"
