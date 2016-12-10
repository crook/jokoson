from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from jokoson.views import api_root, EquipList, EquipDetail, UserList, UserDetail,\
    OrderList, OrderDetail, VendorList, VendorDetail, CategoryList, CategoryDetail,\
    GpssensorList, GpssensorDetail, GpsdataList, GpsdataDetail, UploadFileViewSet, \
    user_and_order_csv_view

from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'file', UploadFileViewSet)

urlpatterns = format_suffix_patterns([
    url(r'^$', api_root),
    url(r'^orders/$',
        OrderList.as_view(),
        name='order-list'),
    url(r'^orders/(?P<pk>[0-9]+)/$',
        OrderDetail.as_view(),
        name='order-detail'),
    url(r'^vendors/$',
        VendorList.as_view(),
        name='vendor-list'),
    url(r'^vendors/(?P<pk>[0-9]+)/$',
        VendorDetail.as_view(),
        name='vendor-detail'),
    url(r'^equips/$',
        EquipList.as_view(),
        name='equip-list'),
    url(r'^equips/(?P<pk>[0-9]+)/$',
        EquipDetail.as_view(),
        name='equip-detail'),
    url(r'^users/$',
        UserList.as_view(),
        name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$',
        UserDetail.as_view(),
        name='user-detail'),
    url(r'^gpssensors/$',
        GpssensorList.as_view(),
        name='gpssensor-list'),
    url(r'^gpssensors/(?P<pk>[0-9]+)/$',
        GpssensorDetail.as_view(),
        name='gpssensor-detail'),
    url(r'^gpsdatas/$',
        GpsdataList.as_view(),
        name='gpsdata-list'),
    url(r'^gpsdatas/(?P<pk>[0-9]+)/$',
        GpsdataDetail.as_view(),
        name='gpsdata-detail'),
    url(r'^categories/$',
        CategoryList.as_view(),
        name='category-list'),
    url(r'^categories/(?P<pk>[0-9]+)/$',
        CategoryDetail.as_view(),
        name='category-detail'),
])


# Query URL
urlpatterns += [
    url('^orders/(?P<username>.+)/$', OrderList.as_view()),

]

# Login and logout views for the browsable API
urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
        namespace='rest_framework')),
]

urlpatterns += router.urls

urlpatterns += [
    url('^exportuser/', user_and_order_csv_view )
]
