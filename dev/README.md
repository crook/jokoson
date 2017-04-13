# How to debug django

Run local server without threading and run use pdb.
    python manager.py runserver --nothreading


# Tips
1) restart 'jokoson-rest' service in case of 'jokoson-db' is not ready.
docker-compose restart jokoson-rest

2) Monior service logs

docker-compose logs -f


3) AttributeError: This QueryDict instance is immutable

http://stackoverflow.com/questions/12611345/django-why-is-the-request-post-object-immutable


class QueryDict

QueryDict instances are immutable, unless you create a copy() of them. That means you 
can't change attributes of request.POST and request.GET directly.


4) QueryDict retun list

https://docs.djangoproject.com/en/dev/ref/request-response/#django.http.QueryDict.getlist
