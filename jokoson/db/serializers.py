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
        depth = 2

    def create(self, validated_data):
        user = super(TenantSerializer, self).create(validated_data)
        # It is necessary to set the password explictly.
        user.set_password(validated_data['password'])
        user.save()

        return user

    def is_valid(self, raise_exception=False):
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

    def export(self, data, model, export_dict):
        pass


class ManufactureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Manufacture
        fields = '__all__'
        depth = 1

    def is_valid(self, raise_exception=False):
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

    def export(self, data, model, export_dict):
        pass


class ModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Model
        fields = '__all__'
        depth = 1

    def is_valid(self, raise_exception=False):
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

    def export(self, data, model, export_dict):
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
        depth = 2

    def is_valid(self, raise_exception=False):
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

    def export(self, equip, mapper, export_dict):
        header = export_dict['header']
        if equip['status'] == 1:
            return

        info = {
            'Equip': {},
            'Model': {},
            'Manufacture': {},
        }

        for item in mapper:
            if 'Equip' in item:
                for key, value in item['Equip'].items():
                    if key == 'Model':
                        info['Equip'][key] = equip[value]['name']
                    elif key == 'Manufacture':
                        info['Equip'][key] = equip[value]['name']
                    else:
                        info['Equip'][key] = equip[value]
            if 'Model' in item:
                model = equip['model']
                for key, value in item['Model'].items():
                    if key == 'Manufacture':
                        info['Model'][key] = model[value]['name']
                    else:
                        info['Model'][key] = model[value]
            if 'Manufacture' in item:
                manufacture = equip['manufacture']
                for key, value in item['Manufacture'].items():
                    info['Manufacture'][key] = manufacture[value]

        prop_list = []
        for item in header:
            for model_type, model_prop in info.items():
                if item in model_prop:
                    prop_list.append(info[model_type][item])
                    break
            else:
                prop_list.append(None)

        export_dict['content'].append(prop_list)


class OrderSerializer(serializers.ModelSerializer):
    #tenant = serializers.HyperlinkedRelatedField(many=False,
    #                                             view_name='user-detail',
    #                                             read_only=True)
    equips = EquipSerializer(many=True, read_only=True)

    class Meta:
        model = models.Order
        fields = '__all__'
        depth = 3

    def instance_query(self):
        try:
            if not self.instance:
                self.instance = models.Order.objects.get(
                    tenant__username=self.initial_data['tenant'],
                    equips__sn=self.initial_data['equips'])
        except self.Meta.model.DoesNotExist:
            pass

    def is_valid(self, raise_exception=False):
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

    def export(self, order, mapper, export_dict):
        header = export_dict['header']
        info = {
            'Order': {},
            'Equip': {},
            'Model': {},
            'Manufacture': {},
        }

        # Only support one-equip for each order
        for item in mapper:
            if 'Order' in item:
                for key, value in item['Order'].items():
                    if key == 'Serial Number':
                        info['Order'][key] = order[value][0]['sn']
                    elif key == 'Tenant':
                        info['Order'][key] = order[value]['username']
                    else:
                        info['Order'][key] = order[value]
            if 'Equip' in item:
                equip = order['equips'][0]
                for key, value in item['Equip'].items():
                    if key == 'Model':
                        info['Equip'][key] = equip[value]['name']
                    elif key == 'Manufacture':
                        info['Equip'][key] = equip[value]['name']
                    else:
                        info['Equip'][key] = equip[value]
            if 'Model' in item:
                model = order['equips'][0]['model']
                for key, value in item['Model'].items():
                    if key == 'Manufacture':
                        info['Model'][key] = model[value]['name']
                    else:
                        info['Model'][key] = model[value]
            if 'Manufacture' in item:
                manufacture = order['equips'][0]['manufacture']
                for key, value in item['Manufacture'].items():
                    info['Manufacture'][key] = manufacture[value]

        prop_list = []
        for item in header:
            for model_type, model_prop in info.items():
                if item in model_prop:
                    prop_list.append(info[model_type][item])
                    break
            else:
                prop_list.append(None)

        export_dict['content'].append(prop_list)
