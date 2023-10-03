#!/bin/sh

cd /src;

watchmedo auto-restart \
    --directory=./ \
    --pattern=*.py \
    --recursive -- celery -A core worker -l INFO -E
