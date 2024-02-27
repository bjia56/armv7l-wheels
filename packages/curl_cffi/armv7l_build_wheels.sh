#!/bin/bash

PYTHON3_VERSION=$1

set -e

build_wheel() (
    PY_VER=$1
    mkdir build$PY_VER
    cd build$PY_VER
    pip$PY_VER wheel ..
)

test_wheel() (
    PY_VER=$1
    cd build$PY_VER
    pip$PY_VER install wheelhouse/curl_cffi*manylinux*armv7l.whl
    python$PY_VER -c "import curl_cffi; print(curl_cffi)"
)

repair_wheel() (
    PY_VER=$1
    cd build$PY_VER
    auditwheel repair curl_cffi*armv7l.whl
)

build_wheel $PYTHON3_VERSION
repair_wheel $PYTHON3_VERSION
test_wheel $PYTHON3_VERSION
