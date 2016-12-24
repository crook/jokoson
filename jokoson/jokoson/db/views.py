from django.contrib.auth.models import User
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.exceptions import MethodNotAllowed
from jokoson.db import models
from jokoson.db import serializers
from jokoson.db.filters import TenantFilter, OrderFilter
from jokoson import exception
from jokoson import utils


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.OrderSerializer
    filter_backends = [filters.DjangoFilterBackend, ]
    filter_fields = ('tenant', 'total_cost', 'equip_vendor', 'equip_category')
    filter_class = OrderFilter

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return models.Order.objects.all()
        else:
            return models.Order.objects.filter(tenant__id=self.request.user.id)


class EquipViewSet(viewsets.ModelViewSet):
    queryset = models.Equip.objects.all()
    serializer_class = serializers.EquipSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_fields = (
        'sn', 'model', 'status', 'health', 'vendor', 'category', 'gps_status')

    def perform_create(self, serializer):
        if self.request.user.is_superuser:
            serializer.save()
        else:
            raise utils.build_method_not_allow_exception(self.request)

    def perform_destroy(self, instance):
        if self.request.user.is_superuser:
            instance.delete()
        else:
            raise utils.build_method_not_allow_exception(self.request)


class VendorViewSet(viewsets.ModelViewSet):
    queryset = models.Vendor.objects.all()
    serializer_class = serializers.VendorSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_fields = ('name', 'city', 'cell_phone', 'office_phone')

    def perform_create(self, serializer):
        if self.request.user.is_superuser:
            serializer.save()
        else:
            raise utils.build_method_not_allow_exception(self.request)

    def perform_destroy(self, instance):
        if self.request.user.is_superuser:
            instance.delete()
        else:
            raise utils.build_method_not_allow_exception(self.request)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (permissions.AllowAny,)
    filter_fields = ('name',)

    def perform_create(self, serializer):
        if self.request.user.is_superuser:
            serializer.save()
        else:
            raise utils.build_method_not_allow_exception(self.request)

    def perform_destroy(self, instance):
        if self.request.user.is_superuser:
            instance.delete()
        else:
            raise utils.build_method_not_allow_exception(self.request)


class TenantViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.TenantSerializer
    filter_fields = ('username', 'id', 'email', 'is_staff')
    filter_class = TenantFilter

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        else:
            return User.objects.filter(id=self.request.user.id)
