from setuptools import find_packages, setup

setup(
    name="app1",
    version="1.0",
    packages=find_packages(),
    entry_points={
        "paste.app_factory": [
            "main = app1:main",
        ],
    },
)
