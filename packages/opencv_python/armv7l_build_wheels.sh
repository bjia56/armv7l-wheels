#!/bin/bash

PYTHON3_VERSION=$1
PACKAGE_VERSION=$2

set -e

build_wheel() (
    PY_VER=$1
    VER=$2
    mkdir build$PY_VER
    cd build$PY_VER
    pip$PY_VER wheel --no-deps opencv_python==$VER
)

test_wheel() (
    PY_VER=$1
    cd build$PY_VER
    pip$PY_VER install wheelhouse/opencv_python*manylinux*armv7l.whl
    python$PY_VER -c "import cv2; print(cv2)"
)

repair_wheel() (
    PY_VER=$1
    cd build$PY_VER
    auditwheel repair opencv_python*armv7l.whl
)

build_wheel $PYTHON3_VERSION $PACKAGE_VERSION
repair_wheel $PYTHON3_VERSION
test_wheel $PYTHON3_VERSION
