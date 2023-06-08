FROM python:3.10.10-alpine

RUN pip install poetry
RUN apk add --no-cache libpq

WORKDIR /src

COPY pyproject.toml poetry.lock ./
RUN apk add --virtual build-deps libpq-dev build-base \
    && poetry config virtualenvs.create false \
    && poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi --no-cache --no-root \
    && apk del build-deps

COPY . .
RUN poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi --no-cache

COPY crontab /etc/crontabs/root

WORKDIR /app
EXPOSE 8000

CMD crond && sillypaste serve
