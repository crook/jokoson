FROM python:3.5
#FROM python:2.7

#RUN apt-get update

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
USER root
ADD . /code/

ENV http_proxy http://proxy.vmware.com:3128
ENV https_proxy https://proxy.vmware.com:3128
RUN env

RUN pip install -r ./requirement.txt
#RUN python manage.py makemigrations
#RUN python manage.py migrate

# Load initial test data
#RUN python manage.py shell -c 'from jokoson.utils import create_user; create_user(username="admin", email="admin@163.com", password="zaq12WSX", is_superuser=True)'
#RUN python manage.py loaddata ./jokoson/testfixtures/initial_data.json

#ENTRYPOINT ["python", "./manage.py", "runserver", "0.0.0.0:8888"]
