from django.urls import path
from django.conf.urls import url
from . import views


app_name = 'blogs'

urlpatterns = [
    
    path('new/',views.BlogCreateView.as_view(),name= 'create'),
    path('<int:pk>/<str:slug>/update/',views.BlogUpdateView.as_view(),name ='update'),
    path('<int:pk>/<str:slug>/remove/',views.BlogDeleteView.as_view(),name ='blog_remove'),
   
    # path('<int:pk>/<str:slug>/',views.BlogDetailView.as_view(),name ='blog_detail'),
    path('test/<int:pk>/<str:slug>/',views.single_blog,name ='blog_detail_f'),

    path('testing/<int:pk>/<str:slug>/',views.final_blog,name ='blog_detail_final'),

    path('list/',views.BlogListView.as_view(),name ='blog_list'),
    path('drafts/',views.DraftListView.as_view(template_name="blogs/blog_draft.html"),name='blog_draft_list'),
    path('published/',views.PublishedListView.as_view(template_name="blogs/blog_published.html"),name='blog_publish'),
    # # path('<int:pk>/remove/',views.PostDeleteView.as_view(),name ='post_remove'),
  



    # path('<int:pk>/<str:slug>/like/',views.PostLikeToggle.as_view(),name='like-toggle'),

  
    path('fan/',views.fan,name='fan'),
    path('publish/<int:pk>/<str:slug>/',views.blog_publish,name='blog_publish'),
    # path('featured/',views.featured,name='featured'),
    path('commented/',views.addcomment,name='addcomment'),
    # # path('api/<int:pk>/<str:slug>/like/',views.PostLikeApiToggle.as_view(),name='like-api=toggle'),
    
    # path('new-comment/<int:pk>/',views.CommentCreateView.as_view(),name= 'comment_create'),
    # path('<int:pk>/remove/',views.CommentDeleteView.as_view(),name='comment_remove'),

   
]