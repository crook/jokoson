from django.contrib.auth import get_user_model
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
    QueryParaMapping = {
        'equip_sn': 'equip__sn',
        'equip_model': 'equip__model',
        'category': 'equip__category__name',
        'vendor': 'equip__vendor__name',
    }

    class Meta:
        model = models.Order

    def __init__(self, query_params, queryset, request):
        if query_params:
            query_para = dict()

            for key, value in query_params.dict().items():
                if key in self.QueryParaMapping:
                    query_para[self.QueryParaMapping[key]] = value
                else:
                    query_para[key] = value

            if not request.user.is_staff:
                if ('tenant' in query_para and
                            query_para['tenant'] != request.user.username):
                    # Try to query another tenant, return empty queryset object
                    self.qs = queryset.none()
                    return
                else:
                    query_para.update({'tenant_id': request.user.id})

            self.qs = queryset.filter(**query_para)
        else:
            if request.user.is_staff:
                self.qs = queryset
            else:
                self.qs = queryset


class EquipFilter(object):
    QueryParaMapping = {
        'vendor': 'vendor__name',
        'category': 'category__name',
    }

    class Meta:
        model = models.Equip

    def __init__(self, query_params, queryset, request):
        if query_params:
            query_para = dict()

            for key, value in query_params.dict().items():
                if key in self.QueryParaMapping:
                    query_para[self.QueryParaMapping[key]] = value
                else:
                    query_para[key] = value

            self.qs = queryset.filter(**query_para)
        else:
            self.qs = queryset
