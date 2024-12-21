#!/bin/bash

PACKAGE=$1
PYTHON3_VERSION=$2
PACKAGE_VERSION=$3

set -e

WORKDIR=$(pwd)
select_python $PYTHON3_VERSION
mkdir build${PYTHON3_VERSION}

build_wheel() (
    cd ${WORKDIR}
    cd build${PYTHON3_VERSION}
    pip3 wheel --no-deps ${PACKAGE}==${PACKAGE_VERSION}
)

test_wheel() (
    cd ${WORKDIR}
    cd build${PYTHON3_VERSION}
    pip3 install wheelhouse/${PACKAGE}*manylinux*armv7l.whl
    python3 -c "import ${PACKAGE}; print(${PACKAGE})"
)

repair_wheel() (
    cd ${WORKDIR}
    cd build${PYTHON3_VERSION}
    auditwheel repair numpy*armv7l.whl
)

build_wheel
repair_wheel
test_wheel
