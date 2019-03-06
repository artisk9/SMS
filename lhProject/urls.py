from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from lhProject import views


urlpatterns = [
    url(r'^$', include('school.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^school/', include('school.urls')),
    url(r'^$', views.login_redirect, name='login_redirect'),
    
]

