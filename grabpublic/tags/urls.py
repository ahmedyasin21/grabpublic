from django.urls import path
from django.conf.urls import url
from . import views


app_name = 'tags'

urlpatterns = [
    path('home/',views.TagListView.as_view(),name='all'),
    path('<int:pk>/<str:slug>/detail/post/',views.TagDetailPostView.as_view(),name='tag_detail'),
    path('<int:pk>/<str:slug>/detail/blog/',views.TagDetailBlogView.as_view(),name='tag_detail_blog'),
]
