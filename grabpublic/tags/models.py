from django.db import models
from grabpublic.utils import unique_slug_generator
from django.db.models.signals import pre_save
from django.urls import reverse

class Tag(models.Model):

    title = models.CharField( max_length=150)
    slug = models.SlugField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)


    

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("tags:tag_detail", kwargs={"pk": self.pk,slug:self.slug})

        
def tag_pre_save_reciever(sender,instance,*args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(tag_pre_save_reciever,Tag)


