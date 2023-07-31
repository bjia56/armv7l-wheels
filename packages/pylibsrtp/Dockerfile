FROM ghcr.io/bjia56/armv7l-wheel-builder:main
ARG PYTHON_VERSION
ARG VERSION
ARG OUTPUT_DIR

WORKDIR /
RUN wget https://github.com/aiortc/pylibsrtp/archive/refs/tags/${VERSION}.tar.gz && \
    tar xf ${VERSION}.tar.gz && \
    cd pylibsrtp-${VERSION} && \
    mkdir -p /tmp/vendor && \
    python3.8 scripts/build-libsrtp.py /tmp/vendor

ENV CFLAGS='-I/usr/local/ssl/include -I/tmp/vendor/include'
ENV LDFLAGS='-L/usr/local/ssl/lib -L/tmp/vendor/lib'
ENV LD_LIBRARY_PATH=/tmp/vendor/lib:/usr/local/ssl/lib:$LD_LIBRARY_PATH
ENV PKG_CONFIG_PATH=/tmp/vendor/lib/pkgconfig:/usr/local/ssl/pkgconfig

COPY . /repo

RUN mkdir -p /pylibsrtp
WORKDIR /pylibsrtp
RUN /repo/armv7l_build_wheels.sh ${PYTHON_VERSION} ${VERSION}

RUN mkdir -p ${OUTPUT_DIR} && \
    cp build${PYTHON_VERSION}/wheelhouse/pylibsrtp*manylinux*armv7l.whl ${OUTPUT_DIR}
