from django.db import models

# Create your models here.
class Order(models.Model):
    class Meta:
        ordering = ('signtime',)

    buyer = models.ForeignKey('auth.User', related_name='orders')
    equip = models.ForeignKey('Equip', related_name='orders')
    #TODO: use models.DurationField()??
    # default format is 'iso-8601', othwise set "input_fomrats=YYYY-MM-DDThh:mm:ss"
    signtime = models.DateTimeField(auto_now_add=True)
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    duration = models.IntegerField()
    # We really care about this filed
    money = models.FloatField()
    # FIXME: add more order stuats?
    valid = models.BooleanField(default=True)


class OrderHist(models.Model):
    equip = models.ForeignKey('Equip', related_name='hist')
    order = models.ForeignKey('Order', related_name='hist')


class Vendor(models.Model):
    name = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    cell_phone = models.CharField(max_length=64)
    office_phone = models.CharField(max_length=64, blank=True)
    address1 = models.CharField(max_length=64)
    address2 = models.CharField(max_length=64, blank=True)


class Category(models.Model):
    description = models.TextField(max_length=1024, default='Categoty Description')


class Equip(models.Model):
    class Meta:
        ordering = ('created_date',)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    # Equip Serial Number
    sn = models.CharField(max_length=128, default='The Serial Number')
    # Equip type
    model = models.CharField(max_length=64)
    # Open to sell or not
    public = models.BooleanField(default=False)
    # TODO: Let user to upload file/video to show thie equip
    # image = models.ImageField(upload_to=None)
    # video = models.BinaryField()

    description = models.TextField(max_length=1024, default='Describe this equip')
    vendor = models.ForeignKey('Vendor', related_name='equips')
    category = models.ForeignKey('Category', related_name='equips', blank=True, null=True)


class Gpssensor(models.Model):
    status = models.IntegerField()
    model = models.CharField(max_length=64)
    batterypercent = models.IntegerField()
    equip = models.ForeignKey('Equip', related_name='gpssensors')
    vendor = models.ForeignKey('Vendor', related_name='gpssensors')
    category = models.ForeignKey('Category', related_name='gpssensors')


class Gpsdata(models.Model):
    time = models.DateTimeField()
    x = models.FloatField()
    y = models.FloatField()
    height = models.FloatField()
    sensor = models.ForeignKey('Gpssensor', related_name='gpsdatas')


class UploadFile(models.Model):
    #Todo: 1)Change the name uploaded file to hash code
    #Todo: 2)Do real data import job after upload
    csvfile = models.FileField()