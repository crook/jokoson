from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import DeviceList, DeviceDetail, UserList, UserDetail

urlpatterns = [
    url(r'^devices/$', DeviceList.as_view()),
    url(r'^devices/(?P<pk>[0-9])/$', DeviceDetail.as_view()),
    url(r'^users/$', UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
