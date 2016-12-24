from django.db import models


# Order information to include the following information
#   Tenant - The client to use the equipment
#   Equip  - The equipment
#   starttime  - the time the tenant start to use the equipment
#   endtime    - the time the tenant will return the equipment
#   duration   - endtime - starttime
#   total_cost - the cost of the rental of the equipment
#   valid      - the order is valid or not
class Order(models.Model):
    class Meta:
        ordering = ('signtime',)

    tenant = models.ForeignKey('auth.User', related_name='orders')
    equip = models.ForeignKey('Equip', related_name='orders')
    # Default format is 'iso-8601',
    # Othwise set "input_fomrats=YYYY-MM-DDThh:mm:ss"
    signtime = models.DateTimeField(auto_now_add=True)
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()
    duration = models.DurationField()
    # We really care about this filed
    total_cost = models.FloatField()
    # FIXME: add more order stuats?
    valid = models.BooleanField(default=True)


# Equipment manufacture information
#    name - name of the equipment manufacture
#    city - city of the equipment manufacture
#    cell_phone   - cell_phone of the equipment manufacture
#    offcie_phone - office phone of the equipment manufacture
#    adddress     - the address of the equipment manufacture
class Vendor(models.Model):
    name = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    cell_phone = models.CharField(max_length=64)
    office_phone = models.CharField(max_length=64, blank=True)
    address = models.CharField(max_length=1024)


# Equipment type
#    name - the type name of the equipment, for example, star-10
#    description
class Category(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=1024,
                                   default='Categoty Description')


# Equipment information to include GPS information
#    sn - the serial number of the equipment
#    model - the model of the equipment
#    status - the status of the equipment, for example, sell, rent or available
#    health - health of the equipment, for example, ok, broken or having issue
#    description - the description of the equipment
#    vendor - the equipment manufacture information and refer to model `Vendor`
#    category - the type name of the equipment and refer to model `Category`
#    gps_status - GPS status which is on the equipment. It may be empty.
#    gps_model  - GPS model which is on the equipment. It may be empty.
#    gps_batterypercent - GPS battery percentage. It may be empty.
#    gps_time - GPS time
#    x, y, z  - GPS information, x - latitude, y - longitude, z - altitude
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
    status = models.IntegerField()
    health = models.TextField(default='OK')
    # TODO: Let user to file file/video to show thie equip
    # image = models.ImageField(upload_to=None)
    # video = models.BinaryField()

    description = models.TextField(max_length=1024,
                                   default='Describe this equip')
    vendor = models.ForeignKey('Vendor', related_name='equips')
    category = models.ForeignKey('Category', related_name='equips', blank=True,
                                 null=True)
    gps_status = models.IntegerField()
    gps_model = models.CharField(max_length=64)
    gps_batterypercent = models.IntegerField()
    gps_time = models.DateTimeField()
    x = models.FloatField()
    y = models.FloatField()
    z = models.FloatField()