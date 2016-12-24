from django.contrib.auth import get_user_model
from django.db.models import QuerySet

from jokoson.db import models


class TenantFilter(object):
    class Meta:
        model = get_user_model()

    def __init__(self, query_params, queryset, request):
        if query_params:
            query_para = query_params.dict()
            if not request.user.is_staff:
                if ('username' in query_para and
                        query_para['username'] != request.user.username):
                    # Try to query another tenant, return empty queryset object
                    self.qs = queryset.none()
                    return
                else:
                    query_para.update({'username': request.user.username})

            self.qs = queryset.filter(**query_para)
        else:
            if request.user.is_staff:
                self.qs = queryset
            else:
                self.qs = queryset.filter(username=request.user.username)


class OrderFilter(object):
    class Meta:
        model = models.Order

    def __init__(self, query_params, queryset, request):
        if query_params:
            self.qs = queryset.filter(**query_params.dict())
        else:
            if request.user.is_staff:
                self.qs = queryset
            else:
                tenant = {'tenant': request.user.username}
                self.qs = queryset.filter(**tenant)
