from django.urls import reverse
from django.db import models
from django.contrib import auth
# from django.db.models.signals import post_save
# from django.dispatch import receiver

# Create your models here.

class User(auth.models.User,auth.models.PermissionsMixin):
    
    def __str__(self):
        return "@{}".format(self.username)


# class UserProfile(models.Model):

#     user = models.OneToOneField(auth.models.User, on_delete=models.CASCADE)
#     avatar = models.ImageField(("Avatar"), upload_to='displays', default = '1.jpg',height_field=None, width_field=None, max_length=None,blank = True)
   

#     def __str__(self):
#         return f'{self.user.username} UserProfile'

#     def get_absolute_url(self):
#         return reverse("userprofile_detail", kwargs={"pk": self.pk})

# @receiver(post_save, sender=User)
# def create_profile(sender, created,instance,**kwargs):
#     if created:
#         UserProfile.objects.create(user=instance)

# @receiver(post_save, sender=User)
# def save_profile(sender, instance,**kwargs):
#     instance.userprofile.save()