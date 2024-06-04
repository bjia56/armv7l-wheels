FROM ghcr.io/bjia56/armv7l-wheel-builder:main
ARG PYTHON_VERSION
ARG VERSION
ARG OUTPUT_DIR

COPY . /repo

ENV CC=/opt/rh/devtoolset-10/root/usr/bin/gcc
ENV FC=/opt/rh/devtoolset-10/root/usr/bin/gfortran5
ENV CXX=/opt/rh/devtoolset-10/root/usr/bin/g++
ENV LD=/opt/rh/devtoolset-10/root/usr/bin/ld
ENV PATH=/opt/rh/devtoolset-10/root/usr/bin:$PATH

WORKDIR /
RUN select_python ${PYTHON_VERSION}
RUN python3 -m pip install numpy --extra-index-url https://bjia56.github.io/armv7l-wheels/ --prefer-binary
RUN mkdir lapx
WORKDIR lapx
RUN /repo/armv7l_build_wheels.sh ${PYTHON_VERSION} ${VERSION}

RUN mkdir -p ${OUTPUT_DIR} && \
    cp build${PYTHON_VERSION}/wheelhouse/lapx*manylinux*armv7l.whl ${OUTPUT_DIR}