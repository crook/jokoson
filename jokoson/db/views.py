from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework import mixins

from jokoson.db import models
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
        try:
            manufacture = models.Manufacture.objects.get(
                id=serializer.initial_data['manufacture'])
        except ValueError:
            manufacture = models.Manufacture.objects.get(
                name=serializer.initial_data['manufacture'])

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
        try:
            manufacture = models.Manufacture.objects.get(
                id=serializer.initial_data['manufacture'])
        except ValueError:
            manufacture = models.Manufacture.objects.get(
                name=serializer.initial_data['manufacture'])

        try:
            model = models.Model.objects.get(
                id=serializer.initial_data['model'])
        except ValueError:
            model = models.Model.objects.get(
                name=serializer.initial_data['model'])

        serializer.save(manufacture=manufacture, model=model)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = (jksn_permissions.OrderPermission,)
    filter_class = jksn_filters.OrderFilter
    filter_fields = (
        'tenant', 'total_cost', 'equip_manufacture', 'equip_category')

    def perform_create(self, serializer):
        equip = models.Equip.objects.get(
            sn=serializer.initial_data['equip_sn'])

        try:
            tenant = get_user_model().objects.get(
                id=serializer.initial_data['tenant'])
        except ValueError:
            tenant = get_user_model().objects.get(
                username=serializer.initial_data['tenant'])

        serializer.save(equip=equip, tenant=tenant)


class CSVViewSet(mixins.CreateModelMixin,
                 viewsets.GenericViewSet):
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
        pass

    def get_viewset(self, name):
        return self.ViewSetMap[name]
