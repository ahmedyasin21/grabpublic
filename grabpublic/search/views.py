from django.shortcuts import render
from profiles.models import UserProfile
from django.views.generic import ListView
from django.db.models import Q
# Create your views here.

class SearchProductListView(ListView):
    model = UserProfile
    template_name = "search/view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get('q')
        return context
    
    def get_queryset(self,*args, **kwargs):
        request = self.request
        method_dict = request.GET
        query = method_dict.get('q',None)

        if query is not None:
            loopups = Q( user__username__icontains = query)|Q(post__title__icontains = query)#|Q(price__icontains = query)|Q(tag__title__icontains = query)
            return UserProfile.objects.filter(loopups).distinct()
        return UserProfile.objects.most_recent()
    