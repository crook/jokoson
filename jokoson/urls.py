from django.conf.urls import url, include
from django.contrib import admin
from jokoson.db import urls as db_urls

urlpatterns = []
urlpatterns += db_urls.urlpatterns

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
#    url(r'^forgot-password/$', ForgotPasswordFormView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
]
