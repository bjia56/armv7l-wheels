FROM ghcr.io/bjia56/armv7l-wheel-builder:main
ARG PYTHON_VERSION
ARG VERSION
ARG OUTPUT_DIR

RUN mkdir /vips
RUN wget -q https://github.com/libvips/libvips/releases/download/v8.15.2/vips-8.15.2.tar.xz && \
    tar xf vips-*.tar.xz && \
    cd vips-* && \
    meson setup build --prefix=/vips && \
    meson compile && \
    meson install

RUN /repo/armv7l_build_wheels.sh ${PYTHON_VERSION} ${VERSION}

RUN mkdir -p ${OUTPUT_DIR} && \
    cp build${PYTHON_VERSION}/wheelhouse/pyvips*manylinux*armv7l.whl ${OUTPUT_DIR}
