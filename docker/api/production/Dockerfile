#syntax=docker/dockerfile:1
FROM python:3.10-alpine3.18

RUN apk add --update --no-cache gcc g++

RUN pip install PyYAML==6.0.1

COPY ./src /src

WORKDIR /src

COPY ./docker/api/requirements.txt .

RUN mkdir tmp

RUN python3 -m pip install -r requirements.txt

COPY ./docker/api/start.sh /start.sh

RUN chmod +x /start.sh
