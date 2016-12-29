#!/bin/bash -x

mysql -uroot -pwelcome -e 'drop database if exists jokoson; create database if not exists jokoson;'

rm ./jokoson/db/migrations/000*.py
python manage.py makemigrations
python manage.py migrate

python manage.py loaddata ./jokoson/testfixtures/initial_data.json

