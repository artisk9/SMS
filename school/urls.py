from django.conf.urls import url
from django.contrib.auth.views import *
from django import forms
from views import *
from . import views




urlpatterns = [
    url(r'^$', views.index),
    url(r'^attendance/',attendance),
    #url(r'^subject/',subject),
    url(r'^login/',login),
    #url(r'^studprofile/',studprofile),
    #url(r'^admission/',admission),
    url(r'^logout/',logout,{'template_name' : 'school/logout.html'}),
    url(r'^home/',home,{'template_name' : 'school/home.html'}),
    url(r'^register/',views.register, name='register'),
    url(r'^school/',schoolApi),
    url(r'^studentprofile/',studentProfileApi),
    url(r'^department/$',departmentApi),
    url(r'^classes/$', classesApi),
    url(r'^parent/$', parentApi),
    url(r'^subject/$',subjectApi),
    url(r'^exam/$',examApi),
    url(r'^marks/$',subjectMarksApi),
    #url(r'^attendance/$',attendanceApi),
    
    url(r'^teacher/$',teacherApi),

    # url(r'^exam_marks/$', exam_marks , name = 'exam_marks'),
    # url(r'^attendance/$', attendance , name = 'attendance')
]