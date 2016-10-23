from django.contrib import admin

# Register your models here.
from .models import Device, Order

admin.site.register(Device)
admin.site.register(Order)
