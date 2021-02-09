from django.shortcuts import render
from django.views.generic import TemplateView
import notifications
from django.contrib.auth.models import User
# from profiles.models import UserProfile
# Create your views here.


class NotifyView(TemplateView):
    template_name ='notify/notifications.html'
    print('say something i am giving up on you!')
    def view(self, request, *args, **kwargs):
        print('user instance',request.user)
        user = User.objects.get(username=request.user)
        qs = user.notifications.all()
        print(qs,'queryset')
        qs.mark_all_as_read(user) 
        qs.save()
        return user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user)
        qs = user.notifications.all()
        print(qs,'qs')
        qs.mark_all_as_read(user) 
        context["qs"] = qs
        return context
    
    
  





