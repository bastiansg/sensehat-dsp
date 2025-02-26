FROM sensehat-dsp-core

COPY sensehat_dsp /src/sensehat_dsp
COPY requirements.txt pyproject.toml  /src/
RUN --mount=type=bind,source=.git,target=/src/.git \
    uv pip install /src --no-deps --system

ARG API_PORT
WORKDIR /src/sensehat_dsp/api
CMD fastapi run app.py --port ${API_PORT}
