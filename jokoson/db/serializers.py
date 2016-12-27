from django.contrib.auth import get_user_model
from rest_framework import serializers

from jokoson.db import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'

    def validate(self, attrs):
        props = ('name',)
        for prop in props:
            if prop not in attrs:
                return None

        return attrs


class VendorSerializer(serializers.ModelSerializer):
    equips = serializers.HyperlinkedRelatedField(many=True,
                                                 view_name='equip-detail',
                                                 read_only=True)

    class Meta:
        model = models.Vendor
        fields = '__all__'
        depth = 1

    def validate(self, attrs):
        props = ('name', 'city', 'cell_phone', 'office_phone', 'address')
        for prop in props:
            if prop not in attrs:
                return None

        return attrs


class EquipSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Equip
        fields = '__all__'
        depth = 1

    def create(self, validate_data):
        equip = models.Equip(category=self._get_category_by_name(),
                             vendor=self._get_vendor_by_name(),
                             **validate_data)
        equip.save()
        return equip

    def _get_category_by_name(self):
        category_name = self.initial_data.get('category')
        return models.Category.objects.get(name=category_name)

    def _get_vendor_by_name(self):
        vendor_name = self.initial_data.get('vendor')
        return models.Vendor.objects.get(name=vendor_name)

    def validate(self, attrs):
        props = ('sn', 'model', 'status', 'health')
        for prop in props:
            if prop not in attrs:
                return None

        return attrs


class OrderSerializer(serializers.ModelSerializer):
    tenant = serializers.HyperlinkedRelatedField(many=False,
                                                 view_name='user-detail',
                                                 read_only=True)

    class Meta:
        model = models.Order
        fields = '__all__'
        depth = 1

    def create(self, validate_data):
        order = models.Order(equip=self._get_equip_by_sn(),
                             tenant=self._get_tenant_by_username(),
                             **validate_data)
        order.save()
        return order

    def _get_equip_by_sn(self):
        equip_sn = self.initial_data.get('equip_sn')
        return models.Equip.objects.get(sn=equip_sn)

    def _get_tenant_by_username(self):
        tenant = self.initial_data.get('tenant')
        return get_user_model().objects.get(username=tenant)

    def validate(self, data):
        if data['starttime'] > data['endtime']:
            raise serializers.ValidationError(
                "The end time of the order must be after the start time.")
        return data


class TenantSerializer(serializers.ModelSerializer):
    orders = serializers.HyperlinkedRelatedField(many=True,
                                                 view_name='order-detail',
                                                 read_only=True)

    class Meta:
        model = get_user_model()
        fields = '__all__'

    def create(self, validated_data):
        user = super(TenantSerializer, self).create(validated_data)
        # It is necessary to set the password explictly.
        user.set_password(validated_data['password'])
        user.save()

        return user

    def is_valid(self, raise_exception=False):
        for k, v in self.initial_data.items():
            if v == 'None':
                self.initial_data[k] = None

        super(TenantSerializer, self).is_valid(True)

    def validate(self, attrs):
        # Check the mandatory fields for tenant model.
        props = ('username', 'first_name', 'last_name', 'password', 'email')
        for prop in props:
            if prop not in attrs:
                return None

        return attrs
