from django.contrib.auth.models import User
from rest_framework import viewsets
from jokoson.db import models
from jokoson.db import serializers
from jokoson.db import filters as jksn_filters
from jokoson.db import permissions


class OrderViewSet(viewsets.ModelViewSet):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = (permissions.OrderPermission,)
    filter_class = jksn_filters.OrderFilter
    filter_fields = ('tenant', 'total_cost', 'equip_vendor', 'equip_category')


class EquipViewSet(viewsets.ModelViewSet):
    queryset = models.Equip.objects.all()
    serializer_class = serializers.EquipSerializer
    permission_classes = (permissions.EquipPermission,)
    filter_class = jksn_filters.EquipFilter
    filter_fields = (
        'sn', 'model', 'status', 'health', 'vendor', 'category', 'gps_status')


class VendorViewSet(viewsets.ModelViewSet):
    queryset = models.Vendor.objects.all()
    serializer_class = serializers.VendorSerializer
    permission_classes = (permissions.VendorPermission,)
    filter_fields = ('name', 'city', 'cell_phone', 'office_phone')


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (permissions.CategoryPermission,)
    filter_fields = ('name',)


class TenantViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TenantSerializer
    filter_fields = ('username', 'id', 'email', 'is_staff')
    filter_class = jksn_filters.TenantFilter

    def get_queryset(self):
        return User.objects.all()
