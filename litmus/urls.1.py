from django.conf.urls import url
from litmus import views

app_name = 'litmus'
urlpatterns = [
    url(r'^$', views.litmus, name='litmus'),
    url(r'^colorSearch$', views.colorSearch, name='colorSearch'),
    url(r'^colorList$', views.colorList, name='colorList'),
    url(r'^colorRegister$', views.colorRegister, name='colorRegister'),
    url(r'^colorInfo/(?P<pk>\d+)/$', views.colorInfo, name='colorInfo'),
    url(r'^colorDelete/(?P<pk>\d+)/$', views.colorDelete, name='colorDelete'),
    url(r'^colorInitialize$', views.colorInitialize, name='colorInitialize'),
    url(r'^colorBackup$', views.colorBackup, name='colorBackup'),
]