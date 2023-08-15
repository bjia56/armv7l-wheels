FROM ghcr.io/bjia56/armv7l-wheel-builder:main
ARG PYTHON_VERSION
ARG VERSION
ARG OUTPUT_DIR

RUN git clone https://github.com/aiortc/aiortc-codecs.git && \
    cd aiortc-codecs && \
    git checkout 1.6
ENV CIBUILDWHEEL=1

COPY *.patch .

WORKDIR aiortc-codecs
ENV CC=/opt/rh/devtoolset-10/root/usr/bin/gcc
ENV CXX=/opt/rh/devtoolset-10/root/usr/bin/g++
ENV LD=/opt/rh/devtoolset-10/root/usr/bin/g++
RUN git apply ../${VERSION}.patch
RUN python3.8 scripts/build-codecs.py /tmp/vendor
WORKDIR ..

ENV CFLAGS='-I/usr/local/ssl/include -I/tmp/vendor/include'
ENV LDFLAGS='-L/usr/local/ssl/lib -L/tmp/vendor/lib'
ENV LD_LIBRARY_PATH=/tmp/vendor/lib:/usr/local/ssl/lib:$LD_LIBRARY_PATH
ENV PKG_CONFIG_PATH=/tmp/vendor/lib/pkgconfig:/usr/local/ssl/lib/pkgconfig

COPY . /repo

RUN mkdir -p /aiortc
WORKDIR /aiortc
RUN /repo/armv7l_build_wheels.sh ${PYTHON_VERSION} ${VERSION}

RUN mkdir -p ${OUTPUT_DIR} && \
    cp build${PYTHON_VERSION}/wheelhouse/aiortc*manylinux*armv7l.whl ${OUTPUT_DIR}