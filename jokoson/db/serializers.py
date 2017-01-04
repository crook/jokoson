from datetime import datetime
from django.contrib.auth import get_user_model
from rest_framework import serializers
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
            if v in ['None', '']:
                self.initial_data[k] = None

        props = ('username', 'first_name', 'last_name', 'password', 'email')
        Validation.check_missing_property('tenant', props, self.initial_data)

        super(TenantSerializer, self).is_valid(raise_exception)

    def instance_query(self):
        try:
            if not self.instance:
                self.instance = get_user_model().objects.get(
                    username=self.initial_data['tenant'])
        except self.Meta.model.DoesNotExist:
            pass


class ManufactureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Manufacture
        fields = '__all__'
        depth = 1

    def is_valid(self, raise_exception=False):
        for k, v in self.initial_data.items():
            if v in ['None', '']:
                self.initial_data[k] = None

        props = ('name', 'city', 'office_phone', 'address')
        Validation.check_missing_property('manufacture', props,
                                          self.initial_data)

        super(ManufactureSerializer, self).is_valid(raise_exception)

    def instance_query(self):
        try:
            if not self.instance:
                self.instance = models.Manufacture.objects.get(
                    name=self.initial_data['name'])
        except self.Meta.model.DoesNotExist:
            pass


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Model
        fields = '__all__'
        depth = 1

    def is_valid(self, raise_exception=False):
        for k, v in self.initial_data.items():
            if v in ['None', '']:
                self.initial_data[k] = None

        props = ('name',)
        Validation.check_missing_property('model', props, self.initial_data)

        super(ModelSerializer, self).is_valid(raise_exception)

    def instance_query(self):
        try:
            if not self.instance:
                self.instance = models.Model.objects.get(
                    name=self.initial_data['name'])
        except self.Meta.model.DoesNotExist:
            pass


class EquipSerializer(serializers.ModelSerializer):
    model = serializers.HyperlinkedRelatedField(
        many=False, view_name='model-detail', read_only=True)

    manufacture = serializers.HyperlinkedRelatedField(
        many=False, view_name='manufacture-detail', read_only=True)

    class Meta:
        model = models.Equip
        fields = '__all__'
        depth = 1

    def is_valid(self, raise_exception=False):
        for k, v in self.initial_data.items():
            if v in ['None', '']:
                self.initial_data[k] = None

        props = ('sn', 'health')
        Validation.check_missing_property('equip', props, self.initial_data)

        super(EquipSerializer, self).is_valid(raise_exception)

    def instance_query(self):
        try:
            if not self.instance:
                self.instance = models.Equip.objects.get(
                    sn=self.initial_data['sn'])
        except self.Meta.model.DoesNotExist:
            pass


class OrderSerializer(serializers.ModelSerializer):
    tenant = serializers.HyperlinkedRelatedField(many=False,
                                                 view_name='user-detail',
                                                 read_only=True)

    class Meta:
        model = models.Order
        fields = '__all__'
        depth = 1

    def instance_query(self):
        try:
            if not self.instance:
                self.instance = models.Order.objects.get(
                    tenant__username=self.initial_data['tenant'],
                    equip__sn=self.initial_data['equip'])
        except self.Meta.model.DoesNotExist:
            pass

    def is_valid(self, raise_exception=False):
        for k, v in self.initial_data.items():
            if v in ['None', '']:
                self.initial_data[k] = None

        props = ('total_cost', 'starttime', 'endtime')
        Validation.check_missing_property('order', props, self.initial_data)

        if self.initial_data['starttime'] > self.initial_data['endtime']:
            raise serializers.ValidationError(
                "The end time of the order must be after the start time.")

        if ('duration' not in self.initial_data or
                not self.initial_data['duration']):
            t_start = datetime.strptime(self.initial_data['starttime'],
                                        "%Y-%m-%dT%H:%M:%S")
            t_end = datetime.strptime(self.initial_data['endtime'],
                                      "%Y-%m-%dT%H:%M:%S")
            self.initial_data['duration'] = t_end - t_start

        super(OrderSerializer, self).is_valid(raise_exception)
