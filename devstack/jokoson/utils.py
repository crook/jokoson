from __future__ import print_function
#from jokoson.models import Equip, Order, Vendor, Gpssensor, Gpsdata, Category

def create_instance(name, properties):
    """
    return the instance with model name and model properties.
        https://docs.djangoproject.com/en/1.10/ref/models/instances/
        https://docs.djangoproject.com/en/1.10/topics/db/queries/
        https://docs.djangoproject.com/en/1.10/ref/models/querysets/#django.db.models.query.QuerySet.get
            : update_or_create
            : get_or_create
    """
    # Load the model
    instance = None
    try:
        import jokoson.models
        model = getattr(jokoson.models, name)
        # https://docs.djangoproject.com/en/1.10/ref/models/class/
        # https://docs.djangoproject.com/en/1.10/topics/db/managers/
        instance  = model.objects.create(**properties)
        instance.save()
    except ImportError:
        print("Not found class %s in jokoson.models"%name)
    except Exception as err:
        print('Failed to create %s instance'%name)
        from sys import exc_info
        exception_info = exc_info();
        print('Caught exception during execution:')
        print('   Type:      %s' % exception_info[0])
        print('   Value:     %s' % exception_info[1])
        print('   Backtrace: %s' % exception_info[2])

    return instance

# django/contrib/auth/models.py:UserManager
def create_user(username, email=None, password=None, **extra_fields):
    from django.contrib.auth.models import User
    user = User.objects.filter(username=username).first()
    if not user:
        user = User(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()

    return user


def test():
    # TODO: import the test json data from 'test' folder
    cate = create_instance('Category', {'description': 'Hello World'})
    vendorA = create_instance('Vendor', {'name':'Equip Vendor', 'city':'cityA'})
    vendorB = create_instance('Vendor', {'name':'Sensor Vendor', 'city':'cityB'})

    equip = create_instance('Equip', {'sn':'Serial Number', 'model': 'A520', 'description': 'The Des', 'vendor': vendorA, 'category': cate})
    sensor = create_instance('Gpssensor', {'status': 1, 'model': 'model', 'batterypercent': 90, 'equip': equip, 'vendor': vendorB, 'category': cate})
    data = create_instance('Gpsdata', {'time':"2016-01-11T12:12:12Z", 'x': 12.12, 'y':13.13, 'height':100, 'sensor': sensor})
    admin = create_user('admin', email='admin@163.com', password='zaq12WSX', is_superuser=True, is_staff=True)

    order = create_instance('Order', {'buyer':admin, 'equip':equip, "signtime": "2016-10-30T12:44:08.231065Z", "starttime": "2016-01-01T12:00:30Z", "endtime": "2016-05-30T12:00:40Z", "duration": 200, "money": 1001.001, "valid": True})

    instances = [cate, vendorA, vendorB, equip, sensor, data, admin, order]
    assert all(instances)

    for item in instances:
        print('remove %r'%item)
        item.delete()

if __name__ == "__main__":
    #  python3 manage.py shell -c 'from jokoson.utils import test; test()'
    # Or run as standlone django script:

    import os, sys, django
    # The value of DJANGO_SETTINGS_MODULE should be in Python path syntax, 
    # e.g. mysite.settings. Note that the settings module should be 
    # on the Python import search path.
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sys.path.insert(0, BASE_DIR)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "devstack.settings")
    django.setup()
    test()
