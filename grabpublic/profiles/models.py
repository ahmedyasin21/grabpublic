from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.urls import reverse
from PIL import Image
from django.shortcuts import render,redirect,get_object_or_404
from random import randint
from decimal import Decimal
from random import sample
from notifications.signals import notify
from django.utils import timezone

class Rank(models.Model):

    catagory = models.CharField(("Ranked Catagory"), max_length=150)
    create_date = models.DateTimeField(default = timezone.now ,blank=True)

    def __str__(self):
        return self.catagory


    def get_absolute_url(self):
        return reverse("Rank_detail", kwargs={"pk": self.pk})

def rank_pre_save_reciever(sender,instance,*args, **kwargs):
    if not instance.create_date:
        instance.create_date = timezone.now()

pre_save.connect(rank_pre_save_reciever,Rank)

class ProfileManager(models.Manager):
    def toggle_follow(self, request_user,user_id, username_to_toggle):
        profile_ = UserProfile.objects.get(user__username__iexact=request_user.username)
        is_following = False
        follower = profile_.follower.filter(username__iexact=username_to_toggle).first()
        if follower:
            profile_.follower.remove(follower.id)
            actor = User.objects.get(pk=user_id)
            user = User.objects.get(username=username_to_toggle)
        else:
            new_follower = User.objects.get(username__iexact=username_to_toggle)
            profile_.follower.add(new_follower.id)
            actor = User.objects.get(pk=user_id)
            user = User.objects.get(username=username_to_toggle)
            notify.send(actor, recipient=user, verb='follow you')
            is_following = True
        return profile_, is_following
    
    def toggle_close_friend(self,request_user, username_to_toggle):
        profile_ = UserProfile.objects.get(user__username__iexact=request_user.username)
        is_close_friend = False
        close_friend = profile_.close_friends.filter(username__iexact=username_to_toggle).first()
        if close_friend:
            profile_.close_friends.remove(close_friend.id)
        else:
            new_follower = User.objects.get(username__iexact=username_to_toggle)
            profile_.close_friends.add(new_follower.id)
            is_close_friend = True
        return profile_, is_close_friend

    def most_recent(self):
        return self.get_queryset().order_by('-create_date')[:9]

        
class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follower = models.ManyToManyField(User, related_name ='is_following',blank=True,)
    close_friends = models.ManyToManyField(User,related_name='my_close_friends', blank=True)
    rank = models.ManyToManyField(Rank, related_name='rank', default='Newbie', blank=True)

    avatar = models.ImageField(("Avatar"), upload_to='displays', default = '1.jpg',height_field=None, width_field=None, max_length=None,blank = True)
    background =models.ImageField(("background1"), upload_to='backgrounds', default = 'ak.jpg',height_field=None, width_field=None, max_length=None,blank = True)
    background_2 =models.ImageField(("background2"), upload_to='backgrounds', default = 'ak.jpg',height_field=None, width_field=None, max_length=None,blank = True)
    background_3 =models.ImageField(("background3"), upload_to='backgrounds', default = 'ak.jpg',height_field=None, width_field=None, max_length=None,blank = True)
    background_4 =models.ImageField(("background4"), upload_to='backgrounds', default = 'ak.jpg',height_field=None, width_field=None, max_length=None,blank = True)
    background_5 =models.ImageField(("background5"), upload_to='backgrounds', default = 'ak.jpg',height_field=None, width_field=None, max_length=None,blank = True)
    create_date = models.DateField(auto_now_add=True,null=True)
        
    username = models.CharField(null=True,blank=True, max_length=50)
    displayname =models.CharField( max_length=150,blank=True)
    bio = models.TextField(default='I like something',blank=True)

    @property
    def email_address(self):
        return self.user.email

   
    objects = ProfileManager()

    def __str__(self):
        return f'{self.user.username}'
    
    def save(self,*args, **kwargs):
        # user_obj = User.objects.filter(username=self.user.username)
        # print(user_obj,'user object')
        # print(user_obj.email,'email have a user') 
        # email = self.email_address
        # user_obj.email = self.email_address
        # print(user_obj.email,'email have a user') 
        # user_obj.save(user_obj.email)
        super(UserProfile,self).save(*args, **kwargs) #it will take data and save it x

        dp = Image.open(self.avatar.path) #storing avatar in varible
        if dp.height >300 or dp.width >300:
            output_size =(300,300) #set anysize you want
            dp.thumbnail(output_size) 
            dp.save(self.avatar.path) #after resing it save it in data base in place of uploaded once by user
        
       

    def get_absolute_url(self):
        return reverse("profiles:final_detail", kwargs={"username": self.user.username})


def profile_pre_save_reciever(sender,instance,*args, **kwargs):
    if not instance.create_date:
        instance.create_date = timezone.now()

pre_save.connect(rank_pre_save_reciever,UserProfile)
# def create_profile(sender, created,instance,**kwargs):
# def create_profile(sender, created,instance,**kwargs):
@receiver(post_save, sender=User)
def create_profile(sender, created, instance,**kwargs):
    if created:
        all_profiles = UserProfile.objects.all()
        user_followers =instance.is_following.all()
        pk_range = 0
        for profile in all_profiles:
            if not profile in user_followers:
                pk_range +=1
        if pk_range >= 2:
            k1, k2 = sample(range(pk_range), 2)
            follow_donate=[]
            for profile in all_profiles:
                if not profile in user_followers:
                    follow_donate.append(profile)
            f1 = follow_donate[k1]
            f2 = follow_donate[k2]
            userprofile = UserProfile.objects.create(user=instance)
            # userprofile.email_address = instance.email
            instance.is_following.add(f1, f2)
            ranked=Rank.objects.get(catagory='Newbie')
            userprofile.rank.add(ranked)
        else:
            userprofile = UserProfile.objects.create(user=instance)
            ranked=Rank.objects.get(catagory='Newbie')
            userprofile.rank.add(ranked)
            # userprofile.email_address = instance.email
            # userprofile.follower.add(f1.user_id, f2.user_id)

    # if created:
    #     pk_range = UserProfile.objects.latest('pk')
    #     k = randint(0, pk_range.pk)
    #     following = list(
    #         UserProfile.objects.filter(pk__gte=k).order_by('pk').union(
    #             UserProfile.objects.filter(pk__lt=k).order_by('-pk')
    #         )[:2])
    #     userprofile = UserProfile.objects.create(user=instance)
    #     userprofile.follower.add(*following)
    # if created:
        # userprofile = UserProfile.objects.create(user=instance)
        # default_user_profile = UserProfile.objects.get_or_create(user__pk=1)[0]
        # default_user_profile.follower.add(instance)
        # userprofile.follower.add(default_user_profile.user)
        # userprofile.follower.add(2)


@receiver(post_save, sender=User)
def save_profile(sender, instance,**kwargs):
    instance.userprofile.save()
    



# Create your models here.
