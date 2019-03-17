from django.conf.urls import url
from litmus import views

app_name = 'litmus'
urlpatterns = [
    url(r'^$', views.litmus, name='litmus'),
    url(r'^litmusHome$', views.litmusHome, name='litmusHome'),
]