#!/usr/bin/env python3

import os
import pathlib
import re
from typing import List, TypedDict
import yaml

from generate_pypi_links import normalize


CWD = pathlib.Path(__file__).parent.resolve()
PACKAGES_DIR = os.path.join(pathlib.Path(CWD).parent.resolve(), "packages")


class PythonSpec(TypedDict):
    versions: List[str]


class PackageSpec(TypedDict):
    versions: List[str] | str


class BuildSpec(TypedDict):
    strategy: str
    source: str | None
    python: PythonSpec
    package: PackageSpec


def get_packages() -> List[str]:
    return [
        f
        for f in os.listdir(PACKAGES_DIR)
        if os.path.isdir(os.path.join(PACKAGES_DIR, f))
    ]


def main() -> None:
    packages = get_packages()
    pass


if __name__ == "__main__":
    main()
