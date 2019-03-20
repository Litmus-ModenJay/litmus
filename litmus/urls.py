from django.conf.urls import url
from litmus import views

app_name = 'litmus'
urlpatterns = [
    url(r'^$', views.litmus, name='litmus'),
    url(r'^main$', views.main, name='main'),
    url(r'^colorSearch$', views.colorSearch, name='colorSearch'),
    url(r'^colorInfo/(?P<pk>\d+)/$', views.colorInfo, name='colorInfo'),
]