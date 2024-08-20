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
    python_requires=">=3.8.10",
    install_requires=[
        "textual[syntax]",
        "aiodocker~=0.22.1",
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
