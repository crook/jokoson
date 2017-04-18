from django.contrib.auth import get_user_model
import django_filters
from jokoson.db import models


# The Filter class will be called in the following case:
#   1. List view
#   2. Retrieve view
#   3. Destroy view
#   4. Update view
# And it is targeted to filter the right queryset.

class TenantFilter(django_filters.rest_framework.FilterSet):
    class Meta:
        model = get_user_model()
        fields = ('username', 'id', 'email', 'is_staff')
        exclude = ['format', 'password']


class EquipFilter(django_filters.rest_framework.FilterSet):
    manufacture = django_filters.CharFilter(name="manufacture__name")
    model = django_filters.CharFilter(name="model__name")
    #category = django_filters.CharFilter(name="category__name")

    class Meta:
        model = models.Equip
        fields = [
            'sn', 'model', 'status', 'health', 'manufacture', 'gps_status',
        ]
        exclude = ['format']


class OrderFilter(django_filters.rest_framework.FilterSet):
    # TODO: support query by id or name
    equips_model = django_filters.ModelMultipleChoiceFilter(
        name="equips__model__name",
        to_field_name='name',
        lookup_expr='in',
        queryset=models.Model.objects.all()
    )
    equips_manufacture = django_filters.ModelMultipleChoiceFilter(
        name="equips__manufacture__name",
        to_field_name='name',
        lookup_expr='in',
        queryset=models.Manufacture.objects.all()
    )
    equips_sn = django_filters.ModelMultipleChoiceFilter(
        name='equips__sn',
        to_field_name='sn',
        lookup_expr='in',
        queryset=models.Equip.objects.all()
    )

    tenant = django_filters.CharFilter(name="tenant__username")
    #category = django_filters.CharFilter(name="category__name")
    max_cost = django_filters.NumberFilter(name="total_cost", lookup_expr='lte')
    min_cost = django_filters.NumberFilter(name="total_cost", lookup_expr='gte')
    endtime = django_filters.DateFilter(name="endtime", lookup_expr='lte')
    starttime = django_filters.DateFilter(name="starttime", lookup_expr='gte')

    class Meta:
        model = models.Order
        fields = [
            # Support query equip by sn, model, manufacture
            'equips_sn', 'equips_model', 'equips_manufacture',
            'tenant','total_cost', 'max_cost', 'min_cost',
            'starttime', 'endtime'
        ]
        exclude = ['format']
