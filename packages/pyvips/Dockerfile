FROM ghcr.io/bjia56/armv7l-wheel-builder:main
ARG PYTHON_VERSION
ARG VERSION
ARG OUTPUT_DIR

WORKDIR /
RUN select_python ${PYTHON_VERSION}
RUN pip3 install meson
RUN yum -y install glib2-devel expat-devel libjpeg-devel libpng-devel openjpeg-devel libtiff-devel libheif-devel libwebp-devel librsvg2-devel 
RUN mkdir -p /tmp/vendor
RUN wget -q https://github.com/libvips/libvips/releases/download/v8.15.2/vips-8.15.2.tar.xz && \
    tar xf vips-*.tar.xz && \
    cd vips-* && \
    meson setup build --prefix=/tmp/vendor && \
    cd build && \
    meson compile && \
    meson install

ENV CFLAGS='-I/tmp/vendor/include'
ENV LDFLAGS='-L/tmp/vendor/lib'
ENV LD_LIBRARY_PATH=/tmp/vendor/lib:$LD_LIBRARY_PATH
ENV PKG_CONFIG_PATH=/tmp/vendor/lib/pkgconfig

COPY . /repo
RUN /repo/armv7l_build_wheels.sh ${PYTHON_VERSION} ${VERSION}

RUN mkdir -p ${OUTPUT_DIR} && \
    cp build${PYTHON_VERSION}/wheelhouse/pyvips*manylinux*armv7l.whl ${OUTPUT_DIR}
