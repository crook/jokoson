import copy
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import ValidationError
from jokoson.db import models
from jokoson.db.utils import Validation


class TenantSerializer(serializers.ModelSerializer):
    orders = serializers.HyperlinkedRelatedField(many=True,
                                                 view_name='order-detail',
                                                 read_only=True)

    class Meta:
        model = get_user_model()
        fields = '__all__'
        depth = 1

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

        super(TenantSerializer, self).is_valid(raise_exception)

    def validate(self, attrs):
        # Check the mandatory fields for tenant model.
        props = ('username', 'first_name', 'last_name', 'password', 'email')
        Validation.check_missing_property('tenant', props, attrs)

        return attrs

    def instance_query(self):
        pass


class ManufactureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Manufacture
        fields = '__all__'
        depth = 1

    def validate(self, attrs):
        props = ('name', 'city', 'office_phone', 'address')
        Validation.check_missing_property('manufacture', props, attrs)

        return attrs

    def instance_query(self):
        try:
            if not self.instance:
                self.instance = models.Manufacture.objects.get(
                    name=self.initial_data['name'])
        except self.Meta.model.DoesNotExist as ex:
            pass



class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Model
        fields = '__all__'
        depth = 1

    def validate(self, attrs):
        props = ('name',)
        Validation.check_missing_property('model', props, attrs)

        return attrs

    def instance_query(self):
        pass


class EquipSerializer(serializers.ModelSerializer):
    # model = serializers.HyperlinkedRelatedField(
    #     many=False, view_name='model-detail', read_only=True)
    #
    # manufacture = serializers.HyperlinkedRelatedField(
    #     many=False, view_name='manufacture-detail', read_only=True)

    class Meta:
        model = models.Equip
        fields = '__all__'
        depth = 1

    def validate(self, attrs):
        props = ('sn', 'health')
        Validation.check_missing_property('equip', props, attrs)

        return attrs

    def is_valid(self, raise_exception=False):
        for k, v in self.initial_data.items():
            if v == 'None':
                self.initial_data[k] = None

        super(EquipSerializer, self).is_valid(raise_exception)

    def instance_query(self):
        pass


class OrderSerializer(serializers.ModelSerializer):
    tenant = serializers.HyperlinkedRelatedField(many=False,
                                                 view_name='user-detail',
                                                 read_only=True)

    class Meta:
        model = models.Order
        fields = '__all__'
        depth = 1

    def validate(self, data):
        if data['starttime'] > data['endtime']:
            raise serializers.ValidationError(
                "The end time of the order must be after the start time.")
        return data

    def instance_query(self):
        pass
