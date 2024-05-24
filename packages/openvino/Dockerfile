FROM ghcr.io/bjia56/armv7l-wheel-builder:main
ARG PYTHON_VERSION
ARG VERSION
ARG OUTPUT_DIR

ENV CC=/opt/rh/devtoolset-10/root/usr/bin/gcc
ENV FC=/opt/rh/devtoolset-10/root/usr/bin/gfortran5
ENV CXX=/opt/rh/devtoolset-10/root/usr/bin/g++
ENV LD=/opt/rh/devtoolset-10/root/usr/bin/ld

WORKDIR /
RUN select_python ${PYTHON_VERSION} 
RUN python3 -m pip install scons
RUN git clone --recurse-submodules --single-branch --branch=master https://github.com/openvinotoolkit/openvino.git
WORKDIR openvino
RUN mkdir build
WORKDIR build
RUN cmake -DCMAKE_BUILD_TYPE=Release \
          -DENABLE_PYTHON=ON \
          -DPython3_EXECUTABLE=/usr/local/bin/python3 \
          -DARM_COMPUTE_SCONS_JOBS=4 \
          .. && \
    make -j4 
