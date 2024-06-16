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
RUN pip3.8 install cmake==3.29.5.1 --extra-index-url https://bjia56.github.io/armv7l-wheels/
RUN select_python ${PYTHON_VERSION}
RUN python3 -m pip install numpy --extra-index-url https://bjia56.github.io/armv7l-wheels/ --prefer-binary
RUN git clone --recurse-submodules -j4 --single-branch --branch=v${VERSION} https://github.com/Microsoft/onnxruntime.git
WORKDIR onnxruntime
RUN ./build.sh --config Release --build_shared_lib --parallel --compile_no_warning_as_error --skip_submodule_sync --skip_tests --build_wheel --allow_running_as_root
RUN auditwheel repair ./build/Linux/Release/dist/onnxruntime-*.whl
RUN find . | grep whl
RUN mkdir -p ${OUTPUT_DIR} 
RUN cp wheelhouse/onnxruntime-*.whl ${OUTPUT_DIR}

