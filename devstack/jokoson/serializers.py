from rest_framework import serializers
from django.contrib.auth.models import User
from jokoson.models import Equip, Order, Vendor, Category, Gpssensor, Gpsdata, UploadFile

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category 
        fields = '__all__'


class VendorSerializer(serializers.ModelSerializer):
    equips = serializers.HyperlinkedRelatedField(many=True, view_name='equip-detail', read_only=True)
    class Meta:
        model = Vendor
        fields= '__all__'
        depth = 1

    def validate(self, data):
        if not (data['cell_phone'] or data ['office_phone']):
            raise serializers.ValidationError("You must input cell or office phone")
        if not (data['address1'] or data ['address2']):
            raise serializers.ValidationError("You must input at least one address")

        return data

class EquipSerializer(serializers.ModelSerializer):
    category_id = serializers.CharField(required=False)
    vendor_id = serializers.CharField()
    class Meta:
        model = Equip
        #exclude = ('category_id', 'vendor_id', )
        fields = '__all__'
        depth = 1

    def create(self, validate_data):
        # TODO: better user category name
        category_id = validate_data.pop('category_id')
        category = Category.objects.get(pk=category_id)
        vendor_id = validate_data.pop('vendor_id')
        vendor = Vendor.objects.get(pk=vendor_id)
        equip = Equip(category=category, vendor=vendor, **validate_data)
        equip.save()
        return equip


class OrderSerializer(serializers.ModelSerializer):
    equip_id = serializers.CharField()
    buyer = serializers.HyperlinkedRelatedField(many=False, view_name='user-detail', read_only=True)
    class Meta:
        model = Order
        #exclude = ('equip_id',)
        fields = '__all__'
        depth = 1

    def create(self, validate_data):
        equip_id = validate_data.pop('equip_id')
        equip = Equip.objects.get(pk=equip_id)
        order = Order(equip=equip, **validate_data)
        order.save()
        return order

    def validate(self, data):
        if data['starttime'] > data['endtime']:
            raise serializers.ValidationError("end time must occur after start time")
        return data


class UserSerializer(serializers.ModelSerializer):
    orders = serializers.HyperlinkedRelatedField(many=True, view_name='order-detail', read_only=True)
    class Meta:
        model = User
        fields = '__all__'


class GpssensorSerializer(serializers.ModelSerializer):
    equip_id = serializers.CharField()
    category_id = serializers.CharField(required=False)
    vendor_id = serializers.CharField()
    gpsdatas = serializers.HyperlinkedRelatedField(many=True, view_name='gpsdata-detail', read_only=True)
    class Meta:
        model= Gpssensor
        #exclude = ('equip_id', 'category_id', 'vendor_id',)
        fields = '__all__'
        depth = 1

    def create(self, validate_data):
        category_id = validate_data.pop('category_id', None)
        category = Category.objects.get(pk=category_id)
        vendor_id = validate_data.pop('vendor_id', None)
        vendor = Vendor.objects.get(pk=vendor_id)
        equip_id = validate_data.pop('equip_id', None)
        equip = Equip.objects.get(pk=equip_id)
        sensor = Gpssensor(category=category, vendor=vendor, equip=equip, **validate_data)
        sensor.save()
        return sensor

    def validate(self, data):
        return data


class GpsdataSerializer(serializers.ModelSerializer):
    sensor_id = serializers.CharField(required=True)
    #sensor = GpssensorSerializer(read_only=True)
    class Meta:
        model = Gpsdata
        #exclude = ('sensor_id',)
        fields = '__all__'
        depth = 1

    def create(self, validate_data):
        print(validate_data)
        sensor_id = validate_data.pop('sensor_id')
        sensor = Gpssensor.objects.get(pk=sensor_id)
        data = Gpsdata(sensor=sensor, **validate_data)
        data.save()
        return data

    def validate_sensor_id(self, value):
        try:
            sensor = Gpssensor.objects.get(pk=value)
        except:
            raise serializers.ValidationError("Not existed Gpssenor id: %s" %value)
        return value

class UploadFileSerializer(serializers.ModelSerializer):
   class Meta:
       model = UploadFile
       fields = ('pk', 'csvfile')
