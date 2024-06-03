FROM ghcr.io/bjia56/armv7l-wheel-builder:main
ARG PYTHON_VERSION
ARG VERSION
ARG OUTPUT_DIR

ENV CC=/opt/rh/devtoolset-10/root/usr/bin/gcc
ENV FC=/opt/rh/devtoolset-10/root/usr/bin/gfortran5
ENV CXX=/opt/rh/devtoolset-10/root/usr/bin/g++
ENV LD=/opt/rh/devtoolset-10/root/usr/bin/ld
ENV PATH=/opt/rh/devtoolset-10/root/usr/bin:$PATH

WORKDIR /
RUN select_python ${PYTHON_VERSION} 
RUN python3 -m pip install numpy --extra-index-url https://bjia56.github.io/armv7l-wheels/ --prefer-binary
RUN mkdir lap
WORKDIR lap
RUN python3 -m pip install lap==${VERSION}
RUN cp $(pip cache list lap --format=abspath) .
RUN auditwheel repair lap-*.whl && \
    pip3 install ./wheelhouse/lap-*manylinux*armv7l.whl --extra-index-url https://bjia56.github.io/armv7l-wheels/ --prefer-binary && \
    python3 -c "import lap; print(lap)"

RUN mkdir -p ${OUTPUT_DIR} && \
    cp ./wheelhouse/lap-*manylinux*armv7l.whl ${OUTPUT_DIR}
