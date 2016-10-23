from django.db import models

# Create your models here.

DEVICE_STYLE_CHOICES = (
    ('basic', 'BasicDevice'),
    ('advanced', 'AdvancedDevice'),
    ('super', 'SuperDevice'),
)

class Order(models.Model):
    class Meta:
        ordering = ('start_date',)

    buyer = models.ForeignKey('auth.User', related_name='orders')
    #TODO: use models.DurationField()??
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(auto_now_add=True)
    # We really care about this filed
    money = models.FloatField()
    valid = models.BooleanField(default=True)


class Device(models.Model):
    class Meta:
        ordering = ('created_date',)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    # Device Serial Number
    sn = models.CharField(max_length=128, default='XXXX')
    # Device type
    style = models.CharField(choices=DEVICE_STYLE_CHOICES, default='basic', max_length=128)
    # Open to sell or not
    public = models.BooleanField(default=False)
    owner = models.ForeignKey('auth.User', related_name='devices')

