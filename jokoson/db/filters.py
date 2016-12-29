from django.contrib.auth import get_user_model
from jokoson.db import models


# The Filter class will be called in the following case:
#   1. List view
#   2. Retrieve view
#   3. Destroy view
#   4. Update view
# And it is targeted to filter the right queryset.

class TenantFilter(object):
    class Meta:
        model = get_user_model()

    def __init__(self, query_params, queryset, request):
        if query_params:
            query_para = query_params.dict()
            if not request.user.is_staff:
                if ('username' in query_para and
                        query_para['username'] != request.user.username):
                    # Try to query another tenant, set self.qs as
                    # an empty queryset object.
                    self.qs = queryset.none()
                    return
                else:
                    # Only list the tenant for the authenticated user
                    # if 'username' is not in the query_params or 'username'
                    # in query_params is the same as the authenticated user.
                    query_para.update({'username': request.user.username})

            self.qs = queryset.filter(**query_para)
        else:
            if request.user.is_staff:
                # List all the tenants
                self.qs = queryset
            else:
                # Only list the tenant for the authenticated user
                self.qs = queryset.filter(username=request.user.username)


class EquipFilter(object):
    QueryParaMapping = {
        'manufacture': 'manufacture__name',
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
            if request.user.is_staff:
                self.qs = queryset
            else:
                self.qs = queryset.filter(health='OK')


class OrderFilter(object):
    QueryParaMapping = {
        'equip_sn': 'equip__sn',
        'equip_model': 'equip__model',
        'category': 'equip__category__name',
        'manufacture': 'equip__manufacture__name',
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
                self.qs = queryset.filter(tenant_id=request.user.id)
