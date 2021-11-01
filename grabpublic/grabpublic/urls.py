"""grabpublic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include, path
# from . import views
from . import views, settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import notifications.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.HomePage.as_view(template_name ="index.html"),name='home'),
    path('test/',views.TestPage.as_view(),name = 'test'),
    path('thanks/',views.ThanksPage.as_view(),name='thanks'),
    path('main/',views.MainCreate.as_view(),name='main_create'),
    path('about/',views.AboutView.as_view(),name ='about'),

    # builted
    path('accounts/',include('accounts.urls',namespace='accounts')),
    path('accounts/',include('django.contrib.auth.urls')),

   
    # Own Apps
    path('posts/',include('posts.urls',namespace='posts')),  
    path('profiles/',include('profiles.urls',namespace='profiles')), 
    path('search/', include('search.urls',namespace = 'search')),
    path('tags/', include('tags.urls',namespace = 'tags')),
    path('notify/', include('notify.urls',namespace = 'notify')),
    path('blogs/', include('blogs.urls',namespace = 'blogs')),
    path('videos/', include('videos.urls',namespace = 'videos')),
    path('followers/', include('followers.urls',namespace = 'followers')),
    path('inbox/notifications/', include(notifications.urls, namespace='notifications')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
