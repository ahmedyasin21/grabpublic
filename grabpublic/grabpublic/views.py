from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from tags.models import Tag

class TestPage(TemplateView,LoginRequiredMixin):
    template_name = "test.html"


class ThanksPage(TemplateView):
    template_name = "thanks.html"

class MainCreate(TemplateView):
    template_name = "main_create.html"
       

class HomePage(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = Tag.objects.all().order_by('timestamp')
        return context
    



class AboutView(TemplateView):
   template_name = "about.html"