#!/bin/bash

PYTHON3_VERSION=$1
PACKAGE_VERSION=$2

set -e

build_wheel() (
    PY_VER=$1
    VER=$2
    mkdir build$PY_VER
    cd build$PY_VER
    pip$PY_VER wheel --no-deps aiortc==$VER
)

test_wheel() (
    PY_VER=$1
    cd build$PY_VER
    pip$PY_VER install wheelhouse/aiortc*manylinux*armv7l.whl --extra-index-url https://bjia56.github.io/armv7l-wheels/ --prefer-binary
    python$PY_VER -c "import aiortc; print(aiortc)"
)

repair_wheel() (
    PY_VER=$1
    cd build$PY_VER
    auditwheel repair aiortc*armv7l.whl
)

build_wheel $PYTHON3_VERSION $PACKAGE_VERSION
repair_wheel $PYTHON3_VERSION
test_wheel $PYTHON3_VERSION
