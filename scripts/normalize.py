#!/usr/bin/env python3

import re
import sys


def normalize(name: str) -> str:
    """ From PEP503 : https://www.python.org/dev/peps/pep-0503/ """
    return re.sub(r"[-_.]+", "-", name).lower()


if __name__ == "__main__":
    for line in sys.stdin.readlines():
        print(normalize(line.rstrip()))