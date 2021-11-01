from django.db import models
from grabpublic.utils import unique_slug_generator
from django.db.models.signals import pre_save
from django.urls import reverse
import requests
import urllib


YOUTUBE_API_KEY = 'AIzaSyBdeXR_2YF4chIIeywL08JSUm2zcOPTl5o'
# Create your models here.
class Video(models.Model):

    
    title = models.CharField(max_length=255)
    url = models.URLField()
    youtube_id = models.CharField(max_length=255)
    slug = models.SlugField(blank=True)

    
    def save(self,*args,**kwargs):
        
        parse = urllib.parse.urlparse(self.url)
        video_id = urllib.parse.parse_qs(parse.query).get('v')
        if video_id:
            self.youtube_id = video_id[0]
            response = requests.get(f'https://youtube.googleapis.com/youtube/v3/videos?part=snippet&id={video_id[0]}&key={YOUTUBE_API_KEY}')
            json = response.json()
            title = json["items"][0]["snippet"]["title"]
            self.title = title
        super(Video,self).save(*args,**kwargs)
    
        
          
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("videos:video_detail", kwargs={'slug':self.slug})


        
def video_pre_save_reciever(sender,instance,*args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(video_pre_save_reciever,Video)