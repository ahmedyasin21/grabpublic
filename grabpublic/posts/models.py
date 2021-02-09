from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()
from tags.models import Tag
from django.db.models.signals import pre_save
from profiles.models import UserProfile
from django.utils.text import slugify

from mptt.models import MPTTModel, TreeForeignKey
# Create your models here.


class Post(models.Model):

    
    username = models.ForeignKey(UserProfile, on_delete=models.CASCADE,blank=True)
    tag = models.ManyToManyField(Tag, default='People and blog')
    description = models.CharField(('Description'),max_length=250,blank=True)
    title = models.CharField(('Content Title'), max_length=250)
    create_date = models.DateTimeField(default = timezone.now)
    image_data = models.ImageField(upload_to='User_Posts', height_field=None, width_field=None, max_length=None)
    slug = models.SlugField(default="abc")
    likes = models.ManyToManyField(User, blank=True,related_name='post_like')
    features = models.ManyToManyField(User,blank=True,related_name='featured')
    

    def save(self,*args,**kwargs):
        self.slug=slugify(self.title)
        super(Post,self).save(*args,**kwargs)

    def __str__(self):
        return self.title

    def publish(self):
        self.create_date = timezone.now()
        self.save()

    def get_absolute_url(self):
        return reverse("posts:post_detail", kwargs={"pk": self.pk,"slug":self.slug})
    
    def get_like_toggle(self):
        return reverse("posts:like")



def post_pre_save_reciever(sender,instance,*args, **kwargs):
    if not instance.username: 
        print(instance.username.userprofile)
        instance.username.userprofile = instance.user.username

pre_save.connect(post_pre_save_reciever,Post)



class Comment(MPTTModel):
    author = models.ForeignKey(User, related_name='author',
                               on_delete=models.CASCADE, default=None, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')
    post = models.ForeignKey(Post ,related_name='comments', on_delete=models.CASCADE)
    body = models.TextField()
    create_date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)
  
        
    
    class MPTTMeta:
        order_insertion_by = ['create_date']

    def __str__(self):
        return '[Post_Title] : {} - [Comment user] : {}'.format(self.post.title,self.author.username)

    def get_absolute_url(self):
        return reverse("posts:post_detail", kwargs={"pk": self.post_id,"slug":self.post.slug})



    


