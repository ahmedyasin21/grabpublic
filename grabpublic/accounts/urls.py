from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views



app_name = 'accounts'

urlpatterns = [
    path('login/',views.CoustomLoginView.as_view(template_name='accounts/login.html'),name = 'login'),
    path('logout/',auth_views.LogoutView.as_view(),name ='logout'),
    path('signup/',views.SignUp.as_view(),name='signup'),
    # path('user',views.userprofile,name='home')
]



