from setuptools import find_packages, setup

setup(
    name="myns.app1",
    namespace_packages=["myns"],
    version="1.0",
    packages=find_packages(),
    entry_points={
        "paste.app_factory": [
            "main = myns.app1:main",
        ],
    },
)
