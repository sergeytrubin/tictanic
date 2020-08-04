FROM python:3.6-slim

RUN apt-get update && apt-get install -qq -y \
  build-essential libpq-dev --no-install-recommends

RUN mkdir /app
WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
RUN pip install --editable .

LABEL maintainer="Sergey Trubin <sergey.trubin@protonmail.com>"

#CMD gunicorn -b 0.0.0.0:8000 --access-logfile - "tictanic.app:create_app()"
CMD gunicorn -b 0.0.0.0:8000 --access-logfile - "app:create_app()"
