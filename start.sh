#!/bin/bash -x

ROOT_DIR=~
PROJECT=jokoson
mysql_password=welcome
mysql_db=jokoson

echo "mysql-server mysql-server/root_password password $mysql_password" | sudo debconf-set-selections
echo "mysql-server mysql-server/root_password_again password $mysql_password" | sudo debconf-set-selections

sudo apt-get -y install mysql-server
sudo apt-get -y install libmysqlclient-dev

mysql -uroot -p$mysql_password -e "create database if not exists $mysql_db;"

#sudo apt-get update
sudo apt-get -y install python3-pip

sudo pip3 install virtualenv

sudo apt-get -yyq install git

mkdir -p $ROOT_DIR/$PROJECT
cd $ROOT_DIR/$PROJECT
virtualenv $ROOT_DIR/$PROJECT/.env

source $ROOT_DIR/$PROJECT/.env/bin/activate

pip install django

pip install -r requirement.txt
