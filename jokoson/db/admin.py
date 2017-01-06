from django.contrib import admin
# Register your models here.
from jokoson.db import models

admin.site.register(models.Equip)
admin.site.register(models.Order)
admin.site.register(models.Manufacture)
admin.site.register(models.Model)
