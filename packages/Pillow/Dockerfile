FROM ghcr.io/bjia56/armv7l-wheel-builder:main
ARG PYTHON_VERSION
ARG VERSION
ARG OUTPUT_DIR

RUN yum install -y libX11-devel
RUN yum remove -y zlib-devel

ENV PATH=/opt/rh/devtoolset-10/root/usr/bin:$PATH

WORKDIR /
RUN git clone https://github.com/python-pillow/Pillow.git && \
    cd Pillow && \
    git checkout ${VERSION} && \
    git submodule update --init --recursive && \
    export BUILD_PREFIX="/usr/local" && \
    ./.github/workflows/wheels-dependencies.sh

COPY . /repo

ENV PKG_CONFIG_PATH /usr/local/lib/pkgconfig
ENV LDFLAGS -L/usr/local/lib
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib

RUN mkdir -p /Pillow
WORKDIR /Pillow
RUN /repo/armv7l_build_wheels.sh ${PYTHON_VERSION} ${VERSION}

RUN mkdir -p ${OUTPUT_DIR} && \
    cp build${PYTHON_VERSION}/wheelhouse/Pillow*manylinux*armv7l.whl ${OUTPUT_DIR}
