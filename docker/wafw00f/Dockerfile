#syntax=docker/dockerfile:1
FROM python:3.10-alpine3.18

RUN apk update && apk add --update --no-cache gcc g++ make git

RUN git clone https://github.com/EnableSecurity/wafw00f.git /src

WORKDIR /src

COPY docker/wafw00f/entrypoint.sh entrypoint.sh

RUN chmod +x entrypoint.sh && python3 setup.py install

ENTRYPOINT ["/src/entrypoint.sh"]

CMD ["--help"]

