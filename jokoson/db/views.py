from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework import mixins

from django.http import QueryDict
from jokoson.db import models
from jokoson.db import utils
from jokoson.db import serializers
from jokoson.db import filters as jksn_filters
from jokoson.db import permissions as jksn_permissions
from jokoson.csv.csvhandler import CSVHandler


class TenantViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TenantSerializer
    filter_fields = ('username', 'id', 'email', 'is_staff')
    filter_class = jksn_filters.TenantFilter

    def get_queryset(self):
        return get_user_model().objects.all()

    def pre_save(self, obj):
        pass


class ManufactureViewSet(viewsets.ModelViewSet):
    queryset = models.Manufacture.objects.all()
    serializer_class = serializers.ManufactureSerializer
    permission_classes = (jksn_permissions.ManufacturePermission,)
    filter_fields = ('name', 'city', 'cell_phone', 'office_phone')


class ModelViewSet(viewsets.ModelViewSet):
    queryset = models.Model.objects.all()
    serializer_class = serializers.ModelSerializer
    permission_classes = (jksn_permissions.ModelPermission,)
    filter_fields = ('name',)

    def perform_create(self, serializer):
        manufacture = utils.get_object_by_keys('Manufacture',
                value=serializer.initial_data['manufacture'],
                keys=['id', 'name']
        )
        serializer.save(manufacture=manufacture)


class EquipViewSet(viewsets.ModelViewSet):
    queryset = models.Equip.objects.all()
    serializer_class = serializers.EquipSerializer
    permission_classes = (jksn_permissions.EquipPermission,)
    filter_class = jksn_filters.EquipFilter
    filter_fields = (
        'sn', 'model', 'status', 'health', 'manufacture', 'category',
        'gps_status')

    def perform_create(self, serializer):
        manufacture = utils.get_object_by_keys('Manufacture',
                value=serializer.initial_data['manufacture'],
                keys=['id', 'name']
        )
        model = utils.get_object_by_keys('Model',
                value=serializer.initial_data['model'],
                keys=['id', 'name']
        )
        serializer.save(manufacture=manufacture, model=model, status=0)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = (jksn_permissions.OrderPermission,)
    filter_class = jksn_filters.OrderFilter
    # Support query like '/api/order/?equips_manufacture=sn1,sn2'
    filter_fields = (
        'tenant', 'total_cost', 'equips_manufacture', 'equips_category', 'equips_sn')

    def perform_create(self, serializer):
        equips = []
        sns = None
        # TODO: so far only suppory sn
        if isinstance(serializer.initial_data, QueryDict):
            sns = serializer.initial_data.getlist('equips')
        else:
            sns = serializer.initial_data['equips']

        for sn in sns:
            equip = models.Equip.objects.get(sn=sn)

            # TODO: add more equip stauts
            if equip.status != 0:
                raise ValueError(
                    "Invalid equipment %(sn)s status (%(status)s) when "
                    "booking an order." % {
                        'sn': equip.sn,
                        'status': equip.status
                    }
                )
            equip.status = 1
            equip.save(update_fields=['status'])
            equips.append(equip)

        # Set tenant
        tenant = utils.get_object_by_keys(get_user_model(),
                value=serializer.initial_data['tenant'],
                keys=['id', 'username']
        )
        serializer.save(equips=equips, tenant=tenant)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Update the equipment status to 0, which indicates that the equipment
        # is ready for re-rent or sale
        for equip in instance.equips.all():
            equip.status = 0
            equip.save(update_fields=['status'])

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CSVViewSet(mixins.CreateModelMixin,
                 viewsets.ViewSet):
    ViewSetMap = {
        'Manufacture': ManufactureViewSet(),
        'Order': OrderViewSet(),
        'Equip': EquipViewSet(),
        'Model': ModelViewSet(),
    }
    permission_classes = (permissions.IsAdminUser,)

    def create(self, request, *args, **kwargs):
        handler = CSVHandler(self, request.data['datafile'])
        handler.csv_import()
        return Response(status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        handler = CSVHandler(self)
        data = handler.csv_export()
        return Response(data)

    def get_viewset(self, name):
        return self.ViewSetMap[name]
