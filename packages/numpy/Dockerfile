FROM ghcr.io/bjia56/armv7l-wheel-builder:main
ARG PYTHON_VERSION
ARG VERSION
ARG OUTPUT_DIR

ENV CC=/opt/rh/devtoolset-10/root/usr/bin/gcc
ENV FC=/opt/rh/devtoolset-10/root/usr/bin/gfortran5
ENV CXX=/opt/rh/devtoolset-10/root/usr/bin/g++
ENV LD=/opt/rh/devtoolset-10/root/usr/bin/g++

WORKDIR /
RUN wget -q https://github.com/OpenMathLib/OpenBLAS/releases/download/v0.3.23/OpenBLAS-0.3.23.tar.gz && \
    tar xf OpenBLAS-0.3.23.tar.gz && \
    cd OpenBLAS-0.3.23 && \
    mkdir -p /tmp/vendor && \
    make PREFIX=/tmp/vendor TARGET=ARMV7 -j4 && \
    make PREFIX=/tmp/vendor TARGET=ARMV7 install

ENV CFLAGS='-I/usr/local/ssl/include -I/tmp/vendor/include'
ENV LDFLAGS='-L/usr/local/ssl/lib -L/tmp/vendor/lib'
ENV LD_LIBRARY_PATH=/tmp/vendor/lib:/usr/local/ssl/lib:$LD_LIBRARY_PATH
ENV PKG_CONFIG_PATH=/tmp/vendor/lib/pkgconfig:/usr/local/ssl/lib/pkgconfig

COPY . /repo

RUN mkdir /numpy
WORKDIR /numpy
RUN select_python ${PYTHON_VERSION}
RUN /repo/armv7l_build_wheels.sh ${PYTHON_VERSION} ${VERSION}

RUN mkdir -p ${OUTPUT_DIR} && \
    cp build${PYTHON_VERSION}/wheelhouse/numpy*manylinux*armv7l.whl ${OUTPUT_DIR}
