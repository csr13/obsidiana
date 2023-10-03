#syntax=docker/dockerfile:1
FROM python:3.10-alpine3.18

RUN apk update && apk add --update --no-cache gcc g++ git 

RUN python3 -m pip install dirbpy

COPY docker/dirbpy/entrypoint.sh entrypoint.sh

#############################
# this tool needs url lists
#############################

COPY ./docker/dirbpy/files /files

RUN chmod +x entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

CMD ["/bin/echo", "-h"]

