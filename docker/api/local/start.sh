#!/bin/sh

cd /src;

settings="core.configs.dev"



python manage.py makemigrations --settings=$settings;
python manage.py makemigrations users --settings=$settings;
python manage.py makemigrations scan --settings=$settings;
python manage.py makemigrations proxies --settings=$settings;
python manage.py makemigrations ssh --settings=$settings;

python manage.py migrate users --settings=$settings;
python manage.py migrate --settings=$settings;

python manage.py collectstatic --no-input --settings=$settings;
python manage.py create_su --settings=$settings;
python manage.py configure_main_proxy --settings=$settings;


gunicorn \
    --workers=2 \
    --threads=2 \
    --reload \
    --timeout 120 \
    --access-logfile - \
    --bind 0.0.0.0:6969 core.sgi.wsgi:application
