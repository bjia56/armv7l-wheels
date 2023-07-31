FROM ghcr.io/bjia56/armv7l-wheel-builder:main
ARG PYTHON_VERSION
ARG VERSION
ARG OUTPUT_DIR

WORKDIR /
RUN git clone https://github.com/google/crc32c.git && \
    mkdir /tmp/vendor && \
    cd crc32c && \
    git submodule update --init --recursive && \
    git checkout 02e65f4fd3065d27b2e29324800ca6d04df16126 && \
    mkdir build && \
    cd build && \
    cmake -DCMAKE_BUILD_TYPE=Release -DCRC32C_BUILD_TESTS=no -DCRC32C_BUILD_BENCHMARKS=no -DBUILD_SHARED_LIBS=yes -DCMAKE_INSTALL_LIBDIR=lib -DCMAKE_INSTALL_PREFIX=/tmp/vendor .. && \
    make all install && \
    cd ../.. && \
    rm -rf crc32c

ENV CFLAGS='-I/usr/local/ssl/include -I/tmp/vendor/include'
ENV LDFLAGS='-L/usr/local/ssl/lib -L/tmp/vendor/lib'
ENV LD_LIBRARY_PATH=/tmp/vendor/lib:/usr/local/ssl/lib:$LD_LIBRARY_PATH
ENV PKG_CONFIG_PATH=/tmp/vendor/lib/pkgconfig:/usr/local/ssl/pkgconfig

COPY . /repo

RUN mkdir -p /google_crc32c
WORKDIR /google_crc32c
RUN /repo/armv7l_build_wheels.sh ${PYTHON_VERSION} ${VERSION}

RUN mkdir -p ${OUTPUT_DIR} && \
    cp build${PYTHON_VERSION}/wheelhouse/curl_cffi*manylinux*armv7l.whl ${OUTPUT_DIR}
