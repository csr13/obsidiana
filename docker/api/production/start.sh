#!/bin/sh

cd /src;

settings="core.configs.dev"

python manage.py makemigrations --settings=$settings;
python manage.py makemigrations users --settings=$settings;
python manage.py makemigrations scan --settings=$settings;

python manage.py migrate users --settings=$settings;
python manage.py migrate --settings=$settings;

python manage.py collectstatic --no-input --settings=$settings;
python manage.py create_su --settings=$settings;

# Replace with gunicorn
python manage.py runserver 0.0.0.0:6969 --settings=$settings
