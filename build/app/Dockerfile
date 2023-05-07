ARG CORE_IMAGE

FROM ${CORE_IMAGE}

WORKDIR /tmp

# Clean
RUN rm -rf /tmp/*

COPY ./app /root/app
WORKDIR /root/app

CMD ["python", "main.py"]
