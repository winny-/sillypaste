FROM python:3.10-alpine

RUN pip install poetry
RUN apk add --no-cache libpq-dev build-base

WORKDIR /src
COPY . .
RUN poetry config virtualenvs.create false \
  && poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi
COPY crontab /etc/crontabs/root

WORKDIR /app
EXPOSE 8000

CMD crond -l 2 -L /dev/stdout && sillypaste serve