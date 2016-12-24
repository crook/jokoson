from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from jokoson.db import models
from jokoson import exception
from rest_framework.exceptions import MethodNotAllowed
from jokoson import utils


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'

    def is_valid(self, raise_exception=False):
        request = self.context['request']
        if not request.user.is_staff:
            raise utils.build_method_not_allow_exception(request)

        super(CategorySerializer, self).is_valid(True)

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

    def is_valid(self, raise_exception=False):
        request = self.context['request']
        if not request.user.is_staff:
            raise utils.build_method_not_allow_exception(request)

        super(VendorSerializer, self).is_valid(True)

    def validate(self, attrs):
        props = ('name', 'city', 'cell_phone', 'office_phone', 'address')
        for prop in props:
            if prop not in attrs:
                return None

        return attrs


class EquipSerializer(serializers.ModelSerializer):
    category_id = serializers.CharField(required=False)
    vendor_id = serializers.CharField()

    class Meta:
        model = models.Equip
        # exclude = ('category_id', 'vendor_id', )
        fields = '__all__'
        depth = 1

    def create(self, validate_data):
        # TODO: better user category name
        category_id = validate_data.pop('category_id')
        category = models.Category.objects.get(pk=category_id)
        vendor_id = validate_data.pop('vendor_id')
        vendor = models.Vendor.objects.get(pk=vendor_id)
        equip = models.Equip(category=category, vendor=vendor, **validate_data)
        equip.save()
        return equip


class OrderSerializer(serializers.ModelSerializer):
    equip_id = serializers.CharField()
    tenant = serializers.HyperlinkedRelatedField(many=False,
                                                 view_name='user-detail',
                                                 read_only=True)

    class Meta:
        model = models.Order
        # exclude = ('equip_id',)
        fields = '__all__'
        depth = 1

    def create(self, validate_data):
        equip_id = validate_data.pop('equip_id')
        equip = models.Equip.objects.get(pk=equip_id)
        order = models.Order(equip=equip, **validate_data)
        order.save()
        return order

    def validate(self, data):
        if data['starttime'] > data['endtime']:
            raise serializers.ValidationError(
                "end time must occur after start time")
        return data


class TenantSerializer(serializers.ModelSerializer):
    orders = serializers.HyperlinkedRelatedField(many=True,
                                                 view_name='order-detail',
                                                 read_only=True)

    class Meta:
        model = get_user_model()
        fields = '__all__'
        extra_fields = ['owner']

    def create(self, validated_data):
        user = super(TenantSerializer, self).create(validated_data)
        # It is necessary to set the password explictly.
        user.set_password(validated_data['password'])
        user.save()

        return user

    def is_valid(self, raise_exception=False):
        # The attribute `last_login` is mandatory for the data validation.
        # So it is updated here.
        self.initial_data['last_login'] = timezone.now()
        super(TenantSerializer, self).is_valid(True)

    def validate(self, attrs):
        # Check the mandatory fields for tenant model.
        props = ('username', 'first_name', 'last_name', 'password', 'email')
        for prop in props:
            if prop not in attrs:
                return None

        return attrs
