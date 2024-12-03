ARG CORE_IMAGE

FROM ${CORE_IMAGE}

WORKDIR /tmp

# Install app requirements
COPY ./build/api/requirements.txt .
RUN --mount=type=cache,target=/root/.cache \
    pip install -r requirements.txt

# Clean
RUN rm -rf /tmp/*

WORKDIR /root/api
COPY ./api/api.py .
CMD uvicorn api:app --host 0.0.0.0
