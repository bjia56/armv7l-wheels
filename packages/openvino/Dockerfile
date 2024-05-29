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
RUN python3 -m pip install scons
RUN git clone --recurse-submodules --single-branch --branch=${VERSION} https://github.com/openvinotoolkit/openvino.git
WORKDIR openvino
RUN mkdir build
WORKDIR build
RUN cmake -DCMAKE_BUILD_TYPE=Release \
          -DENABLE_PYTHON=ON \
          -DPython3_EXECUTABLE=/usr/local/bin/python3 \
          -DARM_COMPUTE_SCONS_JOBS=4 \
          .. && \
    make -j4 
RUN auditwheel repair /openvino/build/wheelhouse/openvino-*.whl && \
    pip3 install /openvino/build/wheelhouse/openvino-*manylinux*armv7l.whl --extra-index-url https://bjia56.github.io/armv7l-wheels/ --prefer-binary && \
    python3 -c "import openvino; print(openvino)"

RUN mkdir -p ${OUTPUT_DIR} && \
    cp /openvino/build/wheelhouse/openvino-*manylinux*armv7l.whl ${OUTPUT_DIR}
