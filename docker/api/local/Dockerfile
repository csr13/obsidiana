#syntax=docker/dockerfile:1
FROM python:3.10-alpine3.18

RUN apk update

RUN apk add --update --no-cache gcc g++ docker

RUN pip install PyYAML==6.0.1

COPY ./src /src

WORKDIR /src

COPY ./docker/api/requirements.txt .

RUN python3 -m pip install -r requirements.txt

COPY ./docker/api/local/start.sh /start.sh

COPY ./docker/api_tasks/start-monitor.sh /start-monitor.sh

RUN chmod +x /start.sh && chmod +x /start-monitor.sh
