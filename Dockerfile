FROM python:3.13-alpine AS builder

WORKDIR /osbolados

COPY requirements.txt /osbolados
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt

COPY . /osbolados

ENTRYPOINT ["waitress-serve", "--port", "20009", "--url-scheme", "https", "--call", "flasky:create_app"]
VOLUME ["/DATA/configs/lastdeathbot/deaths-database.sqlite:/osbolados/deaths-database.sqlite"]

FROM builder AS installer

RUN apk update && apk add --no-cache sqlite
