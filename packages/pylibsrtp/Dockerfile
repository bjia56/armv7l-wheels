FROM ghcr.io/bjia56/armv7l-wheel-builder:main
ARG PYTHON_VERSION
ARG VERSION
ARG OUTPUT_DIR

ENV CC=/opt/rh/devtoolset-10/root/usr/bin/gcc
ENV FC=/opt/rh/devtoolset-10/root/usr/bin/gfortran5
ENV CXX=/opt/rh/devtoolset-10/root/usr/bin/g++
ENV LD=/opt/rh/devtoolset-10/root/usr/bin/ld

WORKDIR /
RUN select_python ${PYTHON_VERSION} 
RUN wget https://github.com/aiortc/pylibsrtp/archive/refs/tags/${VERSION}.tar.gz && \
    tar xf ${VERSION}.tar.gz && \
    cd pylibsrtp-${VERSION} && \
    mkdir -p /tmp/vendor && \
    python scripts/build-libsrtp.py /tmp/vendor

ENV CFLAGS='-I/usr/local/ssl/include -I/tmp/vendor/include'
ENV LDFLAGS='-L/usr/local/ssl/lib -L/tmp/vendor/lib'
ENV LD_LIBRARY_PATH=/tmp/vendor/lib:/usr/local/ssl/lib:$LD_LIBRARY_PATH
ENV PKG_CONFIG_PATH=/tmp/vendor/lib/pkgconfig:/usr/local/ssl/lib/pkgconfig

COPY . /repo

RUN mkdir -p /pylibsrtp
WORKDIR /pylibsrtp
RUN /repo/armv7l_build_wheels.sh ${PYTHON_VERSION} ${VERSION}

RUN mkdir -p ${OUTPUT_DIR} && \
    cp build${PYTHON_VERSION}/wheelhouse/pylibsrtp*manylinux*armv7l.whl ${OUTPUT_DIR}
