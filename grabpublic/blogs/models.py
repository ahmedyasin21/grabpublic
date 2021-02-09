from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()
from tags.models import Tag
from django.db.models.signals import pre_save
from profiles.models import UserProfile
from django.utils.text import slugify
import re
from mptt.models import MPTTModel, TreeForeignKey
# Create your models here.


class Blog(models.Model):

    
    username = models.ForeignKey(UserProfile, on_delete=models.CASCADE,blank=True)
    tag = models.ManyToManyField(Tag, default='Funny')
    body = models.TextField(('body'),null=True)
    title = models.CharField(('Content Title'), max_length=250)
    create_date = models.DateTimeField(default = timezone.now)
    read_time = models.IntegerField(null=True)
    image_data = models.ImageField(upload_to='User_Posts', height_field=None, width_field=None, max_length=None)
    slug = models.SlugField(default="abc",blank=True)
    fans = models.ManyToManyField(User, blank=True,related_name='fans')
    favorites = models.ManyToManyField(User,blank=True,related_name='favorite')
    published = models.BooleanField(default=False)
    published_date = models.DateTimeField(blank=True,null=True)


    def save(self,*args,**kwargs):
        self.slug=slugify(self.title)
        body_ = self.body
        number_of_words = res = len(re.findall(r'\w+', body_))
        read_time_min=(number_of_words/160)
        if read_time_min < 0.99999:
            read_time_min = 1
        print(number_of_words,'hey there')
        self.read_time = read_time_min
        super(Blog,self).save(*args,**kwargs)

    def __str__(self):
        return self.title

    def publish(self):
        self.published_date = timezone.now()
        self.published = True
        self.save()

    def get_absolute_url(self):
        return reverse("blogs:blog_detail_final", kwargs={"pk": self.pk,"slug":self.slug})
    
    
class Comment(MPTTModel):
    author = models.ForeignKey(User, related_name='blog_author',
                               on_delete=models.CASCADE, default=None, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')
    blog = models.ForeignKey(Blog ,related_name='blog_comments', on_delete=models.CASCADE)
    body = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
  
        
    
    class MPTTMeta:
        order_insertion_by = ['create_date']

    def __str__(self):
        return '[Blog_Title] : {} - [Comment user] : {}'.format(self.blog.title,self.author.username)

    def get_absolute_url(self):
        return reverse("blogs:blog_detail_f", kwargs={"pk": self.blog_id,"slug":self.blog.slug})


def post_pre_save_reciever(sender,instance,*args, **kwargs):
    if not instance.username: 
        print(instance.username.userprofile)
        instance.username.userprofile = instance.user.username

pre_save.connect(post_pre_save_reciever,Blog)





    


