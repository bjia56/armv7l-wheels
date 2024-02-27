FROM ghcr.io/bjia56/armv7l-wheel-builder:main
ARG PYTHON_VERSION
ARG VERSION
ARG OUTPUT_DIR

COPY . /repo

RUN mkdir -p /root/.local/lib/
WORKDIR /root/.local/lib/
RUN wget https://github.com/yifeikong/curl-impersonate/releases/download/v0.6.0/libcurl-impersonate-v0.6.0.arm-linux-gnueabihf.tar.gz && \
    tar -xvf libcurl-impersonate-v0.6.0.arm-linux-gnueabihf.tar.gz

RUN mkdir /curl_cffi
WORKDIR /curl_cffi

RUN LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/root/.local/lib /repo/armv7l_build_wheels.sh ${PYTHON_VERSION} ${VERSION} curl_cffi

RUN mkdir -p ${OUTPUT_DIR} && \
    cp build${PYTHON_VERSION}/wheelhouse/curl_cffi*manylinux*armv7l.whl ${OUTPUT_DIR}
