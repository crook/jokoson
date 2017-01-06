#!/bin/bash -x

docker-compose exec jokoson-rest python manage.py test jokoson.test.user
docker-compose exec jokoson-rest python manage.py test jokoson.test.manufacture
docker-compose exec jokoson-rest python manage.py test jokoson.test.model
docker-compose exec jokoson-rest python manage.py test jokoson.test.equip
docker-compose exec jokoson-rest python manage.py test jokoson.test.order
docker-compose exec jokoson-rest python manage.py test jokoson.test.file
