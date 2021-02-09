from django.urls import path
from django.conf.urls import url
from . import views


app_name = 'videos'

urlpatterns = [
    path('compose/',views.VideoCreateView.as_view(),name='new'),
    path('video/<str:slug>/',views.VideoDetailView.as_view(),name='video_detail'),
    path('search/',views.search_function,name='search_function'),
]
