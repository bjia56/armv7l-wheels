#!/bin/bash

PYTHON3_VERSION=$1
PACKAGE_VERSION=$2
PACKAGE_NAME=$3

set -e

build_wheel() (
    PY_VER=$1
    VER=$2
    PKG=$3
    mkdir build$PY_VER
    cd build$PY_VER
    pip$PY_VER wheel --no-deps $PKG==$VER --no-binary $PKG --extra-index-url https://bjia56.github.io/armv7l-wheels/ --prefer-binary
)

test_wheel() (
    PY_VER=$1
    PKG=$2
    cd build$PY_VER
    pip$PY_VER install wheelhouse/$PKG*manylinux*armv7l.whl --extra-index-url https://bjia56.github.io/armv7l-wheels/ --prefer-binary
    python$PY_VER -c "import cv2; print(cv2)"
)

repair_wheel() (
    PY_VER=$1
    PKG=$2
    cd build$PY_VER
    auditwheel repair $PKG*armv7l.whl
)

build_wheel $PYTHON3_VERSION $PACKAGE_VERSION $PACKAGE_NAME
repair_wheel $PYTHON3_VERSION $PACKAGE_NAME
test_wheel $PYTHON3_VERSION $PACKAGE_NAME
