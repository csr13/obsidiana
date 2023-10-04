#syntax-docker/dockerfile:1
FROM linuxserver/openssh-server:latest

RUN apk update && apk add --update --no-cache gcc \
    g++ \
    python3 \
    python3-dev \
    py3-pip

WORKDIR /src

COPY ./docker/ssh/sshprank .
