FROM debian:bullseye-slim

# OS packages
ARG PYTHON_VERSION
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    unzip \
    curl \
    zsh \
    git-core \
    ca-certificates \
    python${PYTHON_VERSION} \
    python${PYTHON_VERSION}-dev \
    python${PYTHON_VERSION}-distutils \
    python3-setuptools \
    python3-numpy \
    python3-pil \
    python3-smbus \
    gcc \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/tmp/* /var/lib/apt/lists/*

# Set default python version
RUN update-alternatives --install /usr/bin/python python /usr/bin/python${PYTHON_VERSION} 1 \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python${PYTHON_VERSION} 1

WORKDIR /tmp

# Install pip
ARG PIP_VERSION
RUN wget https://github.com/pypa/pip/archive/refs/tags/${PIP_VERSION}.zip \
    && unzip ${PIP_VERSION}.zip \
    && cd pip-${PIP_VERSION} \
    && python setup.py install

# Install sensehat
ARG RTIMULIB_VERSION
ARG SENSEHAT_VERSION
RUN curl -LO https://archive.raspberrypi.org/debian/pool/main/r/rtimulib/librtimulib-dev_${RTIMULIB_VERSION}_arm64.deb \
    && curl -LO https://archive.raspberrypi.org/debian/pool/main/r/rtimulib/librtimulib-utils_${RTIMULIB_VERSION}_arm64.deb \
    && curl -LO https://archive.raspberrypi.org/debian/pool/main/r/rtimulib/librtimulib7_${RTIMULIB_VERSION}_arm64.deb \
    && curl -LO https://archive.raspberrypi.org/debian/pool/main/r/rtimulib/python3-rtimulib_${RTIMULIB_VERSION}_arm64.deb \
    && curl -LO https://archive.raspberrypi.org/debian/pool/main/p/python-sense-hat/python3-sense-hat_${SENSEHAT_VERSION}_all.deb

RUN dpkg -i \
    librtimulib-dev_${RTIMULIB_VERSION}_arm64.deb \
    librtimulib-utils_${RTIMULIB_VERSION}_arm64.deb \
    librtimulib7_${RTIMULIB_VERSION}_arm64.deb \
    python3-rtimulib_${RTIMULIB_VERSION}_arm64.deb \
    python3-sense-hat_${SENSEHAT_VERSION}_all.deb

# Install sensehat_dsp
COPY ./src/sensehat_dsp /tmp/sensehat_dsp
RUN --mount=type=cache,target=/root/.cache \
    pip install ./sensehat_dsp

# Clean
RUN rm -rf /tmp/*

WORKDIR /root
