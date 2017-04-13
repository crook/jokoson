"""jokoson URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from jokoson.db import views
from rest_framework import routers

router = routers.DefaultRouter()
router.root_view_name = 'api'
router.register(r'api/order', views.OrderViewSet, base_name='order')
router.register(r'api/equip', views.EquipViewSet)
router.register(r'api/manufacture', views.ManufactureViewSet)
router.register(r'api/model', views.ModelViewSet, base_name='model')
router.register(r'api/tenant', views.TenantViewSet, base_name='user')
router.register(r'api/csv', views.CSVViewSet, base_name='csv')

urlpatterns = router.urls
