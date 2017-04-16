from rest_framework.serializers import ValidationError
from rest_framework.exceptions import NotFound
from jokoson.db import models
from django.contrib.auth.models import User

def get_object_by_keys(class_or_name, value=None, keys=[]):
    '''return the object by possible keys in order'''
    instance = None

    if isinstance(class_or_name, type(User)):
        model = class_or_name
    else:
        model = getattr(models, class_or_name, None)

    for key in keys:
        try:
            kwargs = {key: value}
            instance = model.objects.get(**kwargs)
            break
        except:
            # possible exception: ValueError, DoesNotExist
            continue
    else:
        raise NotFound(detail='%s payload is not valid' %class_or_name)

    return instance


class Validation(object):
    MESSAGE = ('The %(type)s\'s property %(prop)s should not be empty. '
               'The @(typs)s: %(tenant)s')

    @staticmethod
    def check_missing_property(type, props, attrs):
        error_prop = []
        for prop in props:
            if (prop not in attrs) or (not attrs[prop]):
                error_prop.append(prop)

        if error_prop:
            raise ValidationError(
                detail='The %(type)s\'s property %(prop)s should not be '
                       'empty. The %(type)s: %(attrs)s/' % {
                           'type': type,
                           'prop': error_prop,
                           'attrs': attrs,
                       },
                code='InvalidProperty'
            )
