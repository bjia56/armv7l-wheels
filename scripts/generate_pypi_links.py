#!/usr/bin/env python3

from bs4 import BeautifulSoup
import copy
import os
import pathlib
import re
import requests
import sys
from urllib.parse import urlparse

from normalize import normalize


INDEX_FILE = "index.html"
TEMPLATE_FILE = "pkg_template.html"
CWD = pathlib.Path(__file__).parent.resolve()
PYPI_DIR = os.path.join(pathlib.Path(CWD).parent.resolve(), "pypi")


def package_exists(soup, package_name):
    package_ref = package_name + "/"
    for anchor in soup.find_all('a'):
        if anchor['href'] == package_ref:
            return True
    return False


def update(pkg_name: str, link: str) -> None:
    norm_pkg_name = normalize(pkg_name)

    url = urlparse(link)
    filename = url.path.split('/')[-1]

    # Change the package page
    index_file = os.path.join(PYPI_DIR, norm_pkg_name, INDEX_FILE)
    with open(index_file) as html_file:
        soup = BeautifulSoup(html_file, "html.parser")

    anchors = soup.find_all('a')
    skip_add = False
    for anchor in anchors:
        if anchor['href'] == link:
            return
        if anchor['href'] == "_link":
            anchor['href'] = link
            anchor.contents[0].replace_with(filename)
            skip_add = True

    if not skip_add:
        # Create a new anchor element for our new version
        last_anchor = anchors[-1]  # Copy the last anchor element
        new_anchor = copy.copy(last_anchor)
        new_anchor['href'] = link
        new_anchor.contents[0].replace_with(filename)

        # Add it to our index
        br = soup.new_tag("br")
        last_anchor.insert_after(br)
        br.insert_after(new_anchor)

    # Save it
    with open(index_file, 'wb') as index:
        index.write(soup.prettify("utf-8"))


def register_or_update(pkg_name: str, link: str = None) -> None:
    # Read our index first
    root_index = os.path.join(PYPI_DIR, INDEX_FILE)
    with open(root_index) as html_file:
        soup = BeautifulSoup(html_file, "html.parser")
    norm_pkg_name = normalize(pkg_name)

    if package_exists(soup, norm_pkg_name):
        if link:
            update(pkg_name, link)
        return

    # Create a new anchor element for our new package
    last_anchor = soup.find_all('a')[-1]  # Copy the last anchor element
    new_anchor = copy.copy(last_anchor)
    new_anchor['href'] = "{}/".format(norm_pkg_name)
    new_anchor.contents[0].replace_with(pkg_name)

    # Add it to our index and save it
    last_anchor.insert_after(new_anchor)
    with open(root_index, 'wb') as index:
        index.write(soup.prettify("utf-8"))

    # Then get the template, replace the content and write to the right place
    with open(os.path.join(PYPI_DIR, TEMPLATE_FILE)) as temp_file:
        template = temp_file.read()

    template = template.replace("_package_name", pkg_name)
    if link:
        url = urlparse(link)
        filename = url.path.split('/')[-1]

        template = template.replace("_link", link)
        template = template.replace("_filename", filename)

    os.mkdir(os.path.join(PYPI_DIR, norm_pkg_name))
    package_index = os.path.join(PYPI_DIR, norm_pkg_name, INDEX_FILE)
    with open(package_index, "w") as f:
        f.write(template)


def main() -> None:
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <tag> <package>")
        return

    api = f"https://api.github.com/repos/bjia56/armv7l-wheels/releases/tags/{sys.argv[1]}"
    package = sys.argv[2]

    release = requests.get(api).json()
    if "assets" in release:
        for asset in release["assets"]:
            url = asset["browser_download_url"]
            register_or_update(package, url)
    else:
        print(f"Warning: No release found, but will ensure package directory exists")
        register_or_update(package)


if __name__ == "__main__":
    main()
