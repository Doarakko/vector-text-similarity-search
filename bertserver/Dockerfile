FROM tensorflow/tensorflow:1.12.0-py3

RUN pip install -U pip
RUN pip install --no-cache-dir bert-serving-server
RUN mkdir /app
COPY entrypoint.sh /app

WORKDIR /app
ENTRYPOINT ["/bin/sh", "/app/entrypoint.sh"]
CMD []