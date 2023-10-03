#!/bin/sh

cd /src;

python3 -m celery -A core flower --address=0.0.0.0 --port=5566
