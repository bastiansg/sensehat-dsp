ARG UV_VERSION
FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uv_source

FROM debian:bookworm-slim

ARG PYTHON_VERSION
RUN --mount=type=cache,target=/var/cache/apt \
    --mount=target=/var/cache/apt,type=cache,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    wget \
    unzip \
    curl \
    git-core \
    ca-certificates \
    openssh-client \
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

RUN rm /usr/lib/python${PYTHON_VERSION}/EXTERNALLY-MANAGED
RUN update-alternatives --install /usr/bin/python python /usr/bin/python${PYTHON_VERSION} 1 \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python${PYTHON_VERSION} 1

COPY --from=uv_source /uv /uvx /bin/

WORKDIR /tmp

ARG RTIMULIB_VERSION
ARG SENSEHAT_VERSION
RUN curl -LO https://archive.raspberrypi.org/debian/pool/main/r/rtimulib/librtimulib-dev_${RTIMULIB_VERSION}+bookworm_arm64.deb \
    && curl -LO https://archive.raspberrypi.org/debian/pool/main/r/rtimulib/librtimulib-utils_${RTIMULIB_VERSION}+bookworm_arm64.deb \
    && curl -LO https://archive.raspberrypi.org/debian/pool/main/r/rtimulib/librtimulib7_${RTIMULIB_VERSION}+bookworm_arm64.deb \
    && curl -LO https://archive.raspberrypi.org/debian/pool/main/r/rtimulib/python3-rtimulib_${RTIMULIB_VERSION}+bookworm_arm64.deb \
    && curl -LO https://archive.raspberrypi.org/debian/pool/main/p/python-sense-hat/python3-sense-hat_${SENSEHAT_VERSION}_all.deb

RUN dpkg -i \
    librtimulib-dev_${RTIMULIB_VERSION}+bookworm_arm64.deb \
    librtimulib-utils_${RTIMULIB_VERSION}+bookworm_arm64.deb \
    librtimulib7_${RTIMULIB_VERSION}+bookworm_arm64.deb \
    python3-rtimulib_${RTIMULIB_VERSION}+bookworm_arm64.deb \
    python3-sense-hat_${SENSEHAT_VERSION}_all.deb

COPY ./requirements.txt requirements.txt
RUN --mount=type=ssh \
    mkdir -p -m 0600 ~/.ssh \
    && ssh-keyscan github.com >> ~/.ssh/known_hosts \
    && uv pip install -r requirements.txt --system

RUN rm -rf /tmp/*
WORKDIR /root
