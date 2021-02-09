from django.shortcuts import render
from django.views.generic import CreateView, DeleteView, DetailView, ListView
from .models import Video
from .forms import VideoForm,SearchForm
from django.forms.utils import ErrorList
from django.core.exceptions import ValidationError
from django.http import HttpResponse,JsonResponse
import requests
import urllib


YOUTUBE_API_KEY = 'AIzaSyBdeXR_2YF4chIIeywL08JSUm2zcOPTl5o'

def search_function(request):
    search_form = SearchForm(request.GET)
    if search_form.is_valid():
        # print(search_form.cleaned_data.get('search'),'hest')
        search_encode = search_form.cleaned_data.get('search')
        print(search_encode,'you')
        response = requests.get(f'https://youtube.googleapis.com/youtube/v3/search?part=snippet&maxResults=6&q={search_encode}&key={YOUTUBE_API_KEY}')
        return JsonResponse(response.json())
    return JsonResponse({'error':'not validate form'})

class VideoCreateView(CreateView):
    model = Video
    form_class = VideoForm
   
    template_name = "videos/video_form.html"
    def form_valid(self, form):
        url = form.cleaned_data['url']
        parse = urllib.parse.urlparse(url)
        video_id = urllib.parse.parse_qs(parse.query).get('v')
        print(not 'youtube' in url,'hey')
        if not video_id and not 'youtube' in url:
            return HttpResponse('need to be a youtube video')
        return super().form_valid(form)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        searchform = SearchForm
        context["search_form"] = searchform
        return context
    


class VideoDetailView(DetailView):
    model = Video
    template_name = "videos/video_detail.html"



# Create your views here.

