from django.urls import path
from django.conf.urls import url
from . import views


app_name = 'notify'

urlpatterns = [
    path('',views.NotifyView.as_view(),name='ni'),
]
