FROM python:3.7-alpine as base

FROM base as builder
ARG PANDAS_VERSION=0.23.4
RUN apk add --no-cache python3-dev libstdc++ && \
    apk add --no-cache --virtual .build-deps g++ && \
    ln -s /usr/include/locale.h /usr/include/xlocale.h && \
    pip3 install numpy==1.15.1 && \
    pip3 install pandas==${PANDAS_VERSION} && \
    apk del .build-deps
RUN mkdir /install
WORKDIR /install
COPY requirements.txt /requirements.txt
RUN pip install --install-option="--prefix=/install" -r /requirements.txt

FROM base
COPY --from=builder /install /usr/local

RUN mkdir /app
RUN mkdir /app/src

COPY start.py /app
COPY src /app/src

WORKDIR /app
ENTRYPOINT ["python", "start.py"]