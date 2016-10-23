from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import api_root, DeviceList, DeviceDetail, UserList, UserDetail

urlpatterns = format_suffix_patterns([
    url(r'^$', api_root),
    url(r'^devices/$',
        DeviceList.as_view(),
        name='device-list'),
    url(r'^devices/(?P<pk>[0-9]+)/$',
        DeviceDetail.as_view(),
        name='device-detail'),
    url(r'^users/$',
        UserList.as_view(),
        name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$',
        UserDetail.as_view(),
        name='user-detail')
])

# Login and logout views for the browsable API
urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
        namespace='rest_framework')),
]
