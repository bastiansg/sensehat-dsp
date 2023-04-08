ARG CORE_IMAGE

FROM ${CORE_IMAGE}

WORKDIR /tmp

# Install app requirements
COPY ./build/app/requirements.txt .
RUN --mount=type=cache,target=/root/.cache \
    pip install -r requirements.txt

# Clean
RUN rm -rf /tmp/*

COPY ./app /root/app
WORKDIR /root/app
CMD uvicorn main:app --host 0.0.0.0
