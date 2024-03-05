FROM ghcr.io/bjia56/armv7l-wheel-builder:main
ARG PYTHON_VERSION
ARG VERSION
ARG OUTPUT_DIR

RUN yum install -y libcurl-devel

COPY . /repo

WORKDIR /
RUN git clone https://github.com/lwthiker/curl-impersonate.git && \
    cd curl-impersonate && \
    git checkout 9303ce340f212ba92c00bdfd2f7c1380f1d069d7

WORKDIR /curl-impersonate
RUN mkdir -p build/install
RUN ./configure --prefix=/curl-impersonate/build/install CC=/opt/rh/devtoolset-10/root/usr/bin/gcc CXX=/opt/rh/devtoolset-10/root/usr/bin/g++ && \
    make chrome-build && \
    make chrome-checkbuild && \
    make chrome-install

RUN cp /curl-impersonate/build/install/lib/* /usr/local/lib/

WORKDIR /
RUN git clone https://github.com/yifeikong/curl_cffi.git && \
    cd curl_cffi && \
    git checkout v${VERSION} && \
    touch .so_downloaded && \
    make preprocess

WORKDIR /curl_cffi
RUN LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH /repo/armv7l_build_wheels.sh ${PYTHON_VERSION}

RUN mkdir -p ${OUTPUT_DIR} && \
    cp build${PYTHON_VERSION}/wheelhouse/curl_cffi*manylinux*armv7l.whl ${OUTPUT_DIR}
