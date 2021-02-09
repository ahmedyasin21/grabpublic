from django.urls import path
from django.conf.urls import url
from . import views


app_name = 'followers'

urlpatterns = [
    path('',views.free_10_followers,name='free'),
]
