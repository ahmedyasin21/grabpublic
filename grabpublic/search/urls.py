from django.urls import path
from search.views import SearchProductListView
from . import views

app_name ='search'

urlpatterns = [    
    path('',SearchProductListView.as_view(),name = 'query'),
    
]