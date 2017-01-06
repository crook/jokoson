#! /bin/bash -xe
#
# https://docs.docker.com/compose/

#docker-compose up jokoson-db
#docker-compose up jokoson-rest

# Want to enter this container? Try this:
# docker exec -it dev_jokoson-db_1 bash
# or:
# docker-compose exec -it jokoson-db bash

EXIST=`docker-compose ps -q`
if [ "X" == "X${EXIST}" ]; then
    docker-compose up -d
else
    docker-compose start
fi
