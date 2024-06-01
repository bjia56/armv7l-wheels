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
RUN git clone --recurse-submodules -j4 --single-branch --branch=${VERSION} https://github.com/Microsoft/onnxruntime.git
WORKDIR onnxruntime
RUN ./build.sh --config Release --build_shared_lib --parallel --compile_no_warning_as_error --skip_submodule_sync --build_wheel
RUN find .
