from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'profiles'

urlpatterns = [
    # path('user',UserProfileCreateView.as_view(template_name = 'profiles/userprofile.html'),name='home')
    # path('user/',userprofile,name = 'home'),
    path('user-profile/',views.UserProfileFollowToggle.as_view(),name = 'toggle'),
    path('close-friend/',views.UserProfileCloseFriendToggle.as_view(),name = 'close_friend_toggle'),
    path('user-follow-feed/',views.FollowerHomeView.as_view(),name = 'follow-feed'),

    path('followers/<str:username>/',views.FollowerView.as_view(),name = 'followers'),
    path('followerings/<str:username>/',views.FollowingView.as_view(),name = 'followings'),

    path('profiles/<str:username>/<int:pk>/',views.ProfileUpdateView.as_view(),name = 'update'),

    path('close-friend-feed/',views.CloseFriendHomeView.as_view(),name = 'close-friend-feed'),
    # path('<str:username>/',views.UserProfileDetailView.as_view(),name = 'detail'),
    path('<str:username>/',views.FinalProfileDetailView.as_view(),name = 'detail'),
    path('profiles/hey/', views.ProfileUpdateView.as_view(), name='update'),
    # path('<int:pk>/',UserProfileDetailView.as_view(),name = 'detail'),

    # rank urls 
    path('<str:username>/ranks/',views.RankView.as_view(),name ='rank_detail'),
]
