from django.urls import path
from django.conf.urls import url
from . import views


app_name = 'posts'

urlpatterns = [
    
    path('new/',views.PostCreateView.as_view(),name= 'create'),
   
    path('<int:pk>/<str:slug>/',views.PostDetailView.as_view(),name ='post_detail'),
    path('test/<int:pk>/<str:slug>/',views.single_post,name ='post_detail_f'),

    path('testing/<int:pk>/<str:slug>/',views.final_post,name ='post_detail_final'),

    path('list/',views.PostListView.as_view(),name ='post_list'),
    # path('<int:pk>/remove/',views.PostDeleteView.as_view(),name ='post_remove'),
    path('<int:pk>/<str:slug>/remove/',views.PostDeleteView.as_view(),name ='post_remove'),
    # path('<int:pk>/update/',views.PostUpdateView.as_view(),name ='update'),
    path('<int:pk>/<str:slug>/update/',views.PostUpdateView.as_view(),name ='update'),

    path('<int:pk>/<str:slug>/like/',views.PostLikeToggle.as_view(),name='like-toggle'),

  
    path('like/',views.like,name='like'),
    path('featured/',views.featured,name='featured'),
    path('commented/',views.addcomment,name='addcomment'),
    # path('api/<int:pk>/<str:slug>/like/',views.PostLikeApiToggle.as_view(),name='like-api=toggle'),
    
    path('new-comment/<int:pk>/',views.CommentCreateView.as_view(),name= 'comment_create'),
    path('<int:pk>/remove/',views.CommentDeleteView.as_view(),name='comment_remove'),

   
]

