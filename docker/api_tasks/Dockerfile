#syntax=docker/dockerfile:1
FROM python:3.10-alpine3.18

RUN apk update && apk add --update --no-cache gcc g++ make docker

RUN pip install PyYAML==6.0.1

COPY ./docker/api_tasks/start-worker.sh /start-worker.sh

RUN chmod +x /start-worker.sh

COPY ./src /src

COPY ./docker/api_tasks/install-tools.sh /install-tools.sh

RUN chmod +x install-tools.sh && \
    INSTALL_CVES=no ./install-tools.sh

WORKDIR /src

COPY ./docker/api/requirements.txt .

RUN python3 -m pip install -r requirements.txt

RUN python3 -m pip install watchdog
