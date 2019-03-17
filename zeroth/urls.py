"""zeroth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.litmus, name='litmus')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='litmus')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from litmus import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.litmus, name='litmus'),
    url(r'^litmus$', views.litmus, name='litmus'),
    url(r'^litmus/', include('litmus.urls', namespace='litmus')),
    
]

