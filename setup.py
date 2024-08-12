from glob import glob
from os.path import basename, splitext

from setuptools import find_packages, setup

setup(
    name="swarm-tui",
    version="0.0.1",
    description="",
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    py_modules=[splitext(basename(path))[0] for path in glob("src/*.py")],
    install_requires=[
        "textual",
        "tomlkit>=0.12.3",
        "httpx>=0.26.0",
        "click>=8.1.7",
    ],
    extras_require={
        "dev": ["textual-dev", "pytest==8.0.1", "pytest-cov==4.1.0"],
    },
    entry_points={
        "console_scripts": [
            "swarm-tui=swarm_tui.cli:cli",
        ]
    },
)
