FROM sensehat-dsp-core

RUN --mount=type=cache,target=/var/cache/apt \
    --mount=target=/var/cache/apt,type=cache,sharing=locked \
    apt-get update && apt-get install -y --no-install-recommends \
    vim \
    htop \
    zsh \
    sudo \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/tmp/* /var/lib/apt/lists/*

COPY .devcontainer/requirements.txt .
RUN uv pip install -r requirements.txt --system

ARG DEVCONTAINER_USER
RUN useradd -m $DEVCONTAINER_USER \
    && usermod -aG sudo $DEVCONTAINER_USER \
    && passwd -d $DEVCONTAINER_USER

ENV SHELL=/usr/bin/zsh
RUN chsh $DEVCONTAINER_USER -s $SHELL

WORKDIR /workspace
USER $DEVCONTAINER_USER
RUN sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
