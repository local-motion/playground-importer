FROM python:3.12-alpine as base

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
COPY pandas.txt /pandas.txt
RUN pip install --install-option="--prefix=/install" -r /pandas.txt
RUN ls -lag /install

FROM base
COPY requirements.txt /requirements.txt

COPY --from=builder /install /usr/local
RUN ls -lag /usr/local
RUN pip install --install-option="--prefix=/usr/local" -r /requirements.txt
RUN ls -lag /usr/local

RUN mkdir /app
RUN mkdir /app/src

COPY start.py /app
COPY src /app/src

WORKDIR /app
ENTRYPOINT ["python", "start.py"]