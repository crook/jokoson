from django.contrib import admin

# Register your models here.
from jokoson.models import Equip, Order, OrderHist, Vendor, Category, Gpssensor, Gpsdata

admin.site.register(Equip)
admin.site.register(Order)
#admin.site.register(OrderHist)
admin.site.register(Vendor)
admin.site.register(Category)
admin.site.register(Gpssensor)
admin.site.register(Gpsdata)
