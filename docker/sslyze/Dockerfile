#syntax=docker/dockerfile:1
FROM python:3.10-alpine3.18

RUN python3 -m pip install --upgrade pip setuptools wheel sslyze

COPY ./docker/sslyze/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

