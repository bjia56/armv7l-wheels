#!/usr/bin/env python3

import itertools
import json
import os
import pathlib
import requests
import subprocess
from typing import List, TypedDict
import yaml


CWD = pathlib.Path(__file__).parent.resolve()
PACKAGES_DIR = os.path.join(pathlib.Path(CWD).parent.resolve(), "packages")
BUILDSPEC_FILE = "build.yaml"


class PythonSpec(TypedDict):
    versions: List[str]


class PackageSpec(TypedDict):
    versions: List[str] | str


class DockerSource(TypedDict):
    file: str
    common: bool | None


class BuildSpec(TypedDict):
    strategy: str
    source: str | List[str | DockerSource] | None
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

    data: BuildSpec
    with open(buildspec_file, "r") as file:
        data = yaml.safe_load(file)

    # validations
    if data.get("strategy") not in ["pypi", "dockerfile"]:
        raise Exception(f"invalid strategy: {data['strategy']}")
    if data["strategy"] == "dockerfile":
        if not data.get("source"):
            raise Exception(f"no source(s) specified for Dockerfile build")

        if isinstance(data["source"], list):
            allow_common = True
            for source in data["source"]:
                if isinstance(source, str):
                    allow_common = False
                else:
                    if not source.get("file"):
                        raise Exception("no source file for dict-based Dockerfile build source specification")

                    if source.get("common"):
                        if not allow_common:
                            raise Exception("common Dockerfile sources cannot be listed after non-common sources")
                    else:
                        allow_common = False

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
    res = subprocess.check_output(["git", "tag", "-l", tag]).strip()
    return bool(res)


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
