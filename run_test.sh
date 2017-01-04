#!/bin/bash -x

ROOT_DIR=~
PROJECT=jokoson

cd $ROOT_DIR/$PROJECT

source $ROOT_DIR/$PROJECT/.env/bin/activate

python manage.py test jokoson.test.user
python manage.py test jokoson.test.manufacture
python manage.py test jokoson.test.model
python manage.py test jokoson.test.equip
python manage.py test jokoson.test.order
python manage.py test jokoson.test.file
