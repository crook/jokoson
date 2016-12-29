from rest_framework.serializers import ValidationError


class Validation(object):
    MESSAGE = 'The %(type)s\'s property %(prop)s should not be empty. The @(typs)s: %(tenant)s',

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