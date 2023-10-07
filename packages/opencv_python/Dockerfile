# some of this file was adapted from https://github.com/opencv/opencv-python/blob/e26e6e4611b40ea5344e4e4b6e2467539a07a11f/docker/manylinux2014/Dockerfile_aarch64

FROM ghcr.io/bjia56/armv7l-wheel-builder:main
ARG PYTHON_VERSION
ARG VERSION
ARG OUTPUT_DIR

ARG CCACHE_VERSION=3.7.9
ARG FFMPEG_VERSION=5.1.3
ARG FREETYPE_VERSION=2-13-1
ARG LIBPNG_VERSION=1.6.40
ARG NASM_VERSION=2.15.04
ARG OPENSSL_VERSION=1_1_1u
ARG QT_VERSION=5.15.0
ARG YASM_VERSION=1.3.0

ENV LD_LIBRARY_PATH /usr/local/lib:$LD_LIBRARY_PATH

RUN yum install zlib-devel curl-devel xcb-util-renderutil-devel xcb-util-devel xcb-util-image-devel xcb-util-keysyms-devel xcb-util-wm-devel mesa-libGL-devel libxkbcommon-devel libxkbcommon-x11-devel libXi-devel lapack-devel epel-release -y && \
    yum install dejavu-sans-fonts -y && \
    cp /usr/include/lapacke/lapacke*.h /usr/include/ && \
    curl https://raw.githubusercontent.com/xianyi/OpenBLAS/v0.3.3/cblas.h -o /usr/include/cblas.h && \
    # libpng will be built from source
    yum remove libpng -y

WORKDIR /
RUN mkdir ~/openblas_sources && \
    cd ~/openblas_sources && \
    wget -q https://github.com/OpenMathLib/OpenBLAS/releases/download/v0.3.23/OpenBLAS-0.3.23.tar.gz && \
    tar xf OpenBLAS-0.3.23.tar.gz && \
    cd OpenBLAS-0.3.23 && \
    make PREFIX=/usr/local TARGET=ARMV7 -j4 && \
    make PREFIX=/usr/local TARGET=ARMV7 install

RUN mkdir ~/libpng_sources && \
    cd ~/libpng_sources && \
    curl -O -L https://download.sourceforge.net/libpng/libpng-${LIBPNG_VERSION}.tar.gz && \
    tar -xf libpng-${LIBPNG_VERSION}.tar.gz && \
    cd libpng-${LIBPNG_VERSION} && \
    ./configure --prefix=/usr/local && \
    make && \
    make install && \
    cd .. && \
    rm -rf ~/libpng_sources

RUN mkdir ~/freetype_sources && \
    cd ~/freetype_sources && \
    git clone --depth 1 --branch VER-${FREETYPE_VERSION} https://github.com/freetype/freetype.git && \
    cd freetype && \
    ./configure --prefix="/ffmpeg_build" --enable-freetype-config && \
    make && \
    make install && \
    cd .. && \
    rm -rf ~/freetype_sources

RUN curl -O -L https://download.qt.io/official_releases/qt/5.15/${QT_VERSION}/single/qt-everywhere-src-${QT_VERSION}.tar.xz && \
    tar -xf qt-everywhere-src-${QT_VERSION}.tar.xz && \
    cd qt-everywhere-src-${QT_VERSION} && \
    export MAKEFLAGS=-j$(nproc) && \
    ./configure -prefix /opt/Qt${QT_VERSION} -release -opensource -confirm-license -qtnamespace QtOpenCVPython -xcb -xcb-xlib -bundled-xcb-xinput -no-openssl -no-dbus -skip qt3d -skip qtactiveqt -skip qtcanvas3d -skip qtconnectivity -skip qtdatavis3d -skip qtdoc -skip qtgamepad -skip qtgraphicaleffects -skip qtimageformats -skip qtlocation -skip qtmultimedia -skip qtpurchasing -skip qtqa -skip qtremoteobjects -skip qtrepotools -skip qtscript -skip qtscxml -skip qtsensors -skip qtserialbus -skip qtserialport -skip qtspeech -skip qttranslations -skip qtwayland -skip qtwebchannel -skip qtwebengine -skip qtwebsockets -skip qtwebview -skip xmlpatterns -skip declarative -make libs && \
    make && \
    make install && \
    cd .. && \
    rm -rf qt-everywhere*

ENV QTDIR /opt/Qt${QT_VERSION}
ENV PATH "$QTDIR/bin:$PATH"

RUN mkdir ~/openssl_sources && \
    cd ~/openssl_sources && \
    curl -O -L https://github.com/openssl/openssl/archive/OpenSSL_${OPENSSL_VERSION}.tar.gz && \
    tar -xf OpenSSL_${OPENSSL_VERSION}.tar.gz && \
    cd openssl-OpenSSL_${OPENSSL_VERSION} && \
    ./config --prefix="/ffmpeg_build" --openssldir="/ffmpeg_build" no-pinshared shared zlib && \
    make -j$(getconf _NPROCESSORS_ONLN) && \
    # skip installing documentation
    make install_sw && \
    cd .. && \
    rm -rf ~/openssl_build ~/openssl_sources

RUN mkdir ~/nasm_sources && \
    cd ~/nasm_sources && \
    curl -O -L http://www.nasm.us/pub/nasm/releasebuilds/${NASM_VERSION}/nasm-${NASM_VERSION}.tar.gz && \
    tar -xf nasm-${NASM_VERSION}.tar.gz && cd nasm-${NASM_VERSION} && ./autogen.sh && \
    ./configure --prefix="/ffmpeg_build" --bindir="$HOME/bin" && \
    make -j$(getconf _NPROCESSORS_ONLN) && \
    make install && \
    cd .. && \
    rm -rf ~/nasm_sources

RUN mkdir ~/yasm_sources && \
    cd ~/yasm_sources && \
    curl -O -L http://www.tortall.net/projects/yasm/releases/yasm-${YASM_VERSION}.tar.gz && \
    tar -xf yasm-${YASM_VERSION}.tar.gz && \
    cd yasm-${YASM_VERSION} && \
    ./configure --prefix="/ffmpeg_build" --bindir="$HOME/bin" && \
    make -j$(getconf _NPROCESSORS_ONLN) && \
    make install && \
    cd .. && \
    rm -rf ~/yasm_sources

RUN mkdir ~/libvpx_sources && \
    cd ~/libvpx_sources && \
    git clone --depth 1 https://github.com/webmproject/libvpx.git && \
    cd libvpx && \
    ./configure --prefix="/ffmpeg_build" --disable-examples --disable-unit-tests --enable-vp9-highbitdepth --as=yasm --enable-pic --enable-shared && \
    make -j$(getconf _NPROCESSORS_ONLN) && \
    make install && \
    cd .. && \
    rm -rf ~/libvpx_sources

RUN mkdir ~/ffmpeg_sources && \
    cd ~/ffmpeg_sources && \
    curl -O -L https://ffmpeg.org/releases/ffmpeg-${FFMPEG_VERSION}.tar.gz && \
    tar -xf ffmpeg-${FFMPEG_VERSION}.tar.gz && \
    cd ffmpeg-${FFMPEG_VERSION} && \
    PATH=~/bin:$PATH && \
    PKG_CONFIG_PATH="/ffmpeg_build/lib/pkgconfig" ./configure --prefix="/ffmpeg_build" --extra-cflags="-I/ffmpeg_build/include" --extra-ldflags="-L/ffmpeg_build/lib" --enable-openssl --enable-libvpx --enable-shared --enable-pic --bindir="$HOME/bin" && \
    make -j$(getconf _NPROCESSORS_ONLN) && \
    make install && \
    echo "/ffmpeg_build/lib/" >> /etc/ld.so.conf && \
    ldconfig && \
    rm -rf ~/ffmpeg_sources

RUN curl -O -L https://github.com/ccache/ccache/releases/download/v${CCACHE_VERSION}/ccache-${CCACHE_VERSION}.tar.gz && \
    tar -xf ccache-${CCACHE_VERSION}.tar.gz && \
    cd ccache-${CCACHE_VERSION} && \
    linux32 ./configure && \
    make -j$(getconf _NPROCESSORS_ONLN) && \
    make install && \
    cd .. && \
    rm -rf ccache-${CCACHE_VERSION}.tar.gz

ENV PKG_CONFIG_PATH /usr/local/lib/pkgconfig:/ffmpeg_build/lib/pkgconfig
ENV LDFLAGS -L/ffmpeg_build/lib
ENV PATH "$HOME/bin:$PATH"

COPY . /repo

ENV CC=/opt/rh/devtoolset-10/root/usr/bin/gcc
ENV FC=/opt/rh/devtoolset-10/root/usr/bin/gfortran5
ENV CXX=/opt/rh/devtoolset-10/root/usr/bin/g++
ENV LD=/opt/rh/devtoolset-10/root/usr/bin/g++  

RUN mkdir /opencv_python
WORKDIR /opencv_python
RUN select_python ${PYTHON_VERSION}
RUN /repo/armv7l_build_wheels.sh ${PYTHON_VERSION} ${VERSION}

RUN mkdir -p ${OUTPUT_DIR} && \
    cp build${PYTHON_VERSION}/wheelhouse/opencv_python*manylinux*armv7l.whl ${OUTPUT_DIR}
