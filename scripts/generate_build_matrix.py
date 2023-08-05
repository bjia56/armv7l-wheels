#!/usr/bin/env python3

import itertools
import json
import os
import pathlib
import requests
from typing import List, TypedDict
import yaml


CWD = pathlib.Path(__file__).parent.resolve()
PACKAGES_DIR = os.path.join(pathlib.Path(CWD).parent.resolve(), "packages")
BUILDSPEC_FILE = "build.yaml"


class PythonSpec(TypedDict):
    versions: List[str]


class PackageSpec(TypedDict):
    versions: List[str] | str


class BuildSpec(TypedDict):
    strategy: str
    source: str | List[str] | None
    python: PythonSpec
    package: PackageSpec
    disable: bool | None


def get_packages() -> List[str]:
    packages = [
        f
        for f in os.listdir(PACKAGES_DIR)
        if os.path.isdir(os.path.join(PACKAGES_DIR, f))
    ]
    return sorted(packages)


def load_buildspec(package: str) -> BuildSpec:
    buildspec_file = os.path.join(PACKAGES_DIR, package, BUILDSPEC_FILE)
    if not os.path.isfile(buildspec_file):
        raise Exception(f"BuildSpec file {buildspec_file} not found")

    with open(buildspec_file, "r") as file:
        data: BuildSpec = yaml.safe_load(file)
        return data


def get_python_versions(package: str, buildspec: BuildSpec) -> List[str]:
    return buildspec["python"]["versions"]


def get_package_versions(package: str, buildspec: BuildSpec) -> List[str]:
    if isinstance(buildspec["package"]["versions"], list):
        return buildspec["package"]["versions"]

    if buildspec["package"]["versions"] != "latest":
        return [buildspec["package"]["versions"]]

    latest_version = requests.get(f"https://pypi.org/pypi/{package}/json").json()["info"]["version"]
    return [latest_version]


def already_exists(package: str, version: str, python_version: str) -> bool:
    tag = f"{package}-{version}-cpython{python_version}"
    api = f"https://github.com/bjia56/armv7l-wheels/releases/tag/{tag}"
    req = requests.get(api)
    return req.status_code == 200


def main() -> None:
    packages = get_packages()

    matrix_list = []
    for package in packages:
        buildspec = load_buildspec(package)
        if buildspec.get("disable"):
            continue

        python_versions = get_python_versions(package, buildspec)
        package_versions = get_package_versions(package, buildspec)

        build_list = itertools.product(package_versions, python_versions)

        for build in build_list:
            version, python_version = build[0], build[1]
            if not already_exists(package, version, python_version):
                matrix_list.append(
                    {
                        "package": package,
                        "version": version,
                        "python_version": python_version,
                        "strategy": buildspec["strategy"],
                    }
                )

    print(json.dumps(matrix_list[:50]))


if __name__ == "__main__":
    main()
