#!/bin/sh -x 

cd /code

python manage.py makemigrations
python manage.py migrate
python manage.py loaddata ./jokoson/testfixtures/initial_data.json

#python manage.py runserver 0.0.0.0:8888
python manage.py runserver 0.0.0.0:8888 --nothreading
