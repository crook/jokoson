from __future__ import unicode_literals
from django.utils import six
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList


def _get_error_details(data, default_code=None):
    """
    Descend into a nested data structure, forcing any
    lazy translation strings or strings into `ErrorDetail`.
    """
    if isinstance(data, list):
        ret = [
            _get_error_details(item, default_code) for item in data
            ]
        if isinstance(data, ReturnList):
            return ReturnList(ret, serializer=data.serializer)
        return ret
    elif isinstance(data, dict):
        ret = {
            key: _get_error_details(value, default_code)
            for key, value in data.items()
            }
        if isinstance(data, ReturnDict):
            return ReturnDict(ret, serializer=data.serializer)
        return ret

    text = force_text(data)
    code = getattr(data, 'code', default_code)
    return ErrorDetail(text, code)


def _get_codes(detail):
    if isinstance(detail, list):
        return [_get_codes(item) for item in detail]
    elif isinstance(detail, dict):
        return {key: _get_codes(value) for key, value in detail.items()}
    return detail.code


def _get_full_details(detail):
    if isinstance(detail, list):
        return [_get_full_details(item) for item in detail]
    elif isinstance(detail, dict):
        return {key: _get_full_details(value) for key, value in detail.items()}
    return {
        'message': detail,
        'code': detail.code
    }


class ErrorDetail(six.text_type):
    """
    A string-like object that can additionally
    """
    code = None

    def __new__(cls, string, code=None):
        self = super(ErrorDetail, cls).__new__(cls, string)
        self.code = code
        return self


class APIException(BaseException):
    """
    Base class for REST framework exceptions.
    Subclasses should provide `.status_code` and `.default_detail` properties.
    """
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = _('A server error occurred.')
    default_code = 'error'

    def __init__(self, detail=None, code=None):
        if detail is None:
            detail = self.default_detail
        if code is None:
            code = self.default_code

        self.detail = _get_error_details(detail, code)

    def __str__(self):
        return self.detail

    def get_codes(self):
        """
        Return only the code part of the error details.

        Eg. {"name": ["required"]}
        """
        return _get_codes(self.detail)

    def get_full_details(self):
        """
        Return both the message & code parts of the error details.

        Eg. {"name": [{"message": "This field is required.", "code": "required"}]}
        """
        return _get_full_details(self.detail)


class STATUS(object):
    HTTP_401_UNAUTHORIZED = 401
    HTTP_403_FORBIDDEN = 403


class NoPermissionToCreateEquip(APIException):
    status_code = STATUS.HTTP_403_FORBIDDEN
    default_detail = _(
        'Forbidden or No Permission to create equipment.')
    default_code = 'create_equip_failed'


class NoPermissionToDeleteEquip(APIException):
    status_code = STATUS.HTTP_403_FORBIDDEN
    default_detail = _(
        'Forbidden or No Permission to delete equipment.')
    default_code = 'delete_equip_failed'


class NoPermissionToCreateManufacture(APIException):
    status_code = STATUS.HTTP_403_FORBIDDEN
    default_detail = _(
        'Forbidden or No Permission to create manufacture.')
    default_code = 'create_manufacture_failed'


class NoPermissionToModifyManufacture(APIException):
    status_code = STATUS.HTTP_403_FORBIDDEN
    default_detail = _(
        'Forbidden or No Permission to modify manufacture.')
    default_code = 'modify_manufacture_failed'


class NoPermissionToDeleteManufacture(APIException):
    status_code = STATUS.HTTP_403_FORBIDDEN
    default_detail = _(
        'Forbidden or No Permission to delete manufacture.')
    default_code = 'delete_manufacture_failed'


class NoPermissionToCreateModel(APIException):
    status_code = STATUS.HTTP_403_FORBIDDEN
    default_detail = _(
        'Forbidden or No Permission to create category.')
    default_code = 'create_category_failed'


class NoPermissionToModifyModel(APIException):
    status_code = STATUS.HTTP_403_FORBIDDEN
    default_detail = _(
        'Forbidden or No Permission to modify category.')
    default_code = 'modify_category_failed'


class NoPermissionToDeleteModel(APIException):
    status_code = STATUS.HTTP_403_FORBIDDEN
    default_detail = _(
        'Forbidden or No Permission to delete category.')
    default_code = 'delete_category_failed'
