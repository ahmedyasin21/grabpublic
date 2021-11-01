from django.shortcuts import render,redirect,get_object_or_404
from .models import UserProfile
import json
from posts.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .forms import UserProfileForm,UserUpdateForm
from django.views.generic import TemplateView,CreateView,ListView,DetailView,View,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages,redirects
from django.utils import timezone
from django.http import Http404
from itertools import chain
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db.models import Count
from tags.models import Tag
from profiles.forms import UserUpdateForm
from profiles.models import UserProfile
from notifications.signals import notify

from .models import Rank
# Create your views here.


class ProfileUpdateView(UpdateView):
    refirect_field_name ='profiles:detail'
    form_class = UserUpdateForm
    model = UserProfile

    # def get(self, request, *args, **kwargs):
    #     user = request.user.userprofile
    #     user_notify = User.objects.get(username=self.request.user)
    #     return render(request, "profiles/close_friend.html", {'notify':user_notify.notifications.filter(deleted=False).order_by('-timestamp')[:4]})

    def get_object(self, *args, **kwargs):
        return self.request.user.userprofile
    
    def get_context_data(self, *args, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(*args, **kwargs)
        update_form = UserUpdateForm(instance = self.request.user.userprofile)
        context['form']=update_form

        user = self.request.user.userprofile
        user_notify = User.objects.get(username=self.request.user)
        context['notify'] = user_notify.notifications.filter(deleted=False).order_by('-timestamp')[:4]
        context["notify_count"] = user_notify.notifications.filter(actor_object_id=user_notify.id,deleted=False,unread=True).count()

        return context
    
    def form_valid(self, form):
        if self.request == 'POST':
            form.save()
        return super().form_valid(form)
       


class UserPostListView(LoginRequiredMixin,ListView):
    login_url = '/accounts/login/'
    model = Post
    context_object_name = 'post_list'  
    def get_queryset(self):
        return Post.objects.filter(create_date__lte=timezone.now()).order_by('-create_date')


class UserProfileFollowToggle(LoginRequiredMixin,View):
    login_url = '/accounts/login/'
    def post(self, request):
            username_to_toggle = request.POST.get("user_toggle")
            json_follower = None
            profile_, is_following,json_follower = UserProfile.objects.toggle_follow(request.user, request.user.id ,username_to_toggle,json_follower)
            # json_dump_user = json.loads(json_follower)
            # print(json_dump_user,"Now i views :D")
            return JsonResponse({'result': is_following, 'json_follower':json_follower})
        
  


    


class UserProfileCloseFriendToggle(LoginRequiredMixin,View):
    login_url = '/accounts/login/'

    def post(self, request, *args, **kwargs):
            username_to_toggle = request.POST.get("user")
            profile_, is_close_friend = UserProfile.objects.toggle_close_friend(request.user, username_to_toggle)
            return redirect(f'/profiles/{username_to_toggle}')

    # When working with pk 
    # def post(self, request, *args, **kwargs):
        
        
        # profile_ = UserProfile.objects.get(user=self.request.user)
        # pk = request.POST.get('userprofile_pk')
        # obj = UserProfile.objects.get(pk=pk)

        # if obj.user in profile_.follower.all():
        #     profile_.follower.remove(obj.user)
        # else:
        #     profile_.follower.add(obj.user)
            
class FinalProfileDetailView(LoginRequiredMixin,DetailView):
     
    
    login_url = '/accounts/login/'
    model = UserProfile
    template_name = "profiles/final_userprofile.html"
    # slug_url_kwarg = "username" # this the `argument` in the URL conf
    # slug_field = "user"



    def close_friend(self):
        if self.request.user.is_authenticated:
            if self.request.POST:
                self.object.userprofile.close_friend = True
            else:
                self.object.userprofile.close_friend = False
    



    def get_object(self):
    
        username = self.kwargs.get("username")
        if username is None:
            raise Http404
        return get_object_or_404(User, username__iexact=username, is_active=True)

    
    def get_context_data(self, *args, **kwargs):
       
        
        context = super(FinalProfileDetailView, self).get_context_data(*args, **kwargs)
        user = context['user']
        # user = self.request.POST.get("close")
        # print()
        followers = user.is_following.all()
        # print(followers,'followers')
        following = user.userprofile.follower.count()
        # print(following,'following')
            
        # print(self.request.user.userprofile.follower.all(),'pha')
        is_following = False 
        if user in self.request.user.userprofile.follower.all():
            is_following = True
        context['is_following'] = is_following

        is_close_friend = False   
        if user in self.request.user.userprofile.close_friends.all():
            is_close_friend = True
        context['is_close_friend'] = is_close_friend

        posts = Post.objects.filter(username=user.userprofile).order_by('-create_date')
        print(posts,'hehehehehe')
        context['posts'] = posts

        own=False
        if user.userprofile == self.request.user.userprofile:
            own = True
        context['own'] = own

        user = self.request.user.userprofile
        user_notify = User.objects.get(username=self.request.user)
        context['notify'] = user_notify.notifications.filter(deleted=False).order_by('-timestamp')[:4]
        context["notify_count"] = user_notify.notifications.filter(actor_object_id=user_notify.id,deleted=False,unread=True).count()

        return context   
 

        
            

class UserProfileDetailView(LoginRequiredMixin,DetailView):
     
    
    login_url = '/accounts/login/'
    model = UserProfile
    template_name = "profiles/userprofile_detail.html"
    # slug_url_kwarg = "username" # this the `argument` in the URL conf
    # slug_field = "user"



    def close_friend(self):
        if self.request.user.is_authenticated:
            if self.request.POST:
                self.object.userprofile.close_friend = True
            else:
                self.object.userprofile.close_friend = False
    



    def get_object(self):
    
        username = self.kwargs.get("username")
        if username is None:
            raise Http404
        return get_object_or_404(User, username__iexact=username, is_active=True)

    
    def get_context_data(self, *args, **kwargs):
       
        
        context = super(UserProfileDetailView, self).get_context_data(*args, **kwargs)
        user = context['user']
        # user = self.request.POST.get("close")
        # print()
        followers = user.is_following.count()
        if followers >= 100:
            ranked=Rank.objects.get(catagory='Novice')
            userprofile = UserProfile.objects.get(user=user)
            userprofile.rank.add(ranked)
            userprofile.save()
            user_o = User.objects.get(username='admin')
            actor = user_o
            notify.send(actor, recipient=user, verb=f'Congratulations you have {followers} followers and rank is increase!')
            

        # print(followers,'followers')
        following = user.userprofile.follower.count()
        # print(following,'following')
            
        # print(self.request.user.userprofile.follower.all(),'pha')
        is_following = False 
        if user in self.request.user.userprofile.follower.all():
            is_following = True
        context['is_following'] = is_following

        is_close_friend = False   
        if user in self.request.user.userprofile.close_friends.all():
            is_close_friend = True
        context['is_close_friend'] = is_close_friend

        posts = Post.objects.filter(username=user.userprofile).order_by('-create_date')
        context['posts'] = posts

        own=False
        if user.userprofile == self.request.user.userprofile:
            own = True
        context['own'] = own



        user = self.request.user.userprofile
        user_notify = User.objects.get(username=self.request.user)
        context['notify'] = user_notify.notifications.filter(deleted=False).order_by('-timestamp')[:4]
        context["notify_count"] = user_notify.notifications.filter(actor_object_id=user_notify.id,deleted=False,unread=True).count()

        return context

class FollowerHomeView(LoginRequiredMixin,TemplateView):
   
    login_url = '/accounts/login/'
    template_name = "profiles/follower_home_feed.html"
   

    def get_context_data(self, *args, **kwargs):
        context = super(FollowerHomeView, self).get_context_data(*args, **kwargs)
        request = self.request
        user = request.user.userprofile
        user_notify = User.objects.get(username=self.request.user)
        # print(user.follower.all(),"hehhehehe")
        is_following_user_ids = [x.id for x in user.follower.all()]

        following_qs = []
        for follower in user.follower.all():
            qs = Post.objects.filter(username__user=follower).order_by('-create_date')[:2]
            for post in qs:
                following_qs.append(post)
             
        # followers posts
        # follower_qs = Post.objects.filter(
        #                         username__user__is_following__user=request.user
        #                         ).order_by('-create_date')[:10]

        suggested_follower_query = UserProfile.objects.annotate(num_followers=Count('follower')).order_by('-num_followers')
        # print(suggested_follower_query,"ajajsja")
        follower_array = []
        
        suggested_follower_query_arry = []

        for suggestion in suggested_follower_query:
            # print(suggestion,"suggestion")
            if user != suggestion:
                suggested_follower_query_arry.append(suggestion)
                # print(suggested_follower_query_arry,"suggestion inserted")
            


        for user in user.follower.all():
            # print(user,'user')
            try:
                follower = UserProfile.objects.get(user=user)
                # print(follower,"got a follower")
            except UserProfile.DoesNotExist:
                pass
            
            if follower in suggested_follower_query_arry:
                # print(follower,"follower")
                suggested_follower_query_arry.remove(follower)

        # print(suggested_follower_query_arry,"arry follower")
            
        
        context["object_list"]= following_qs[:10]
        context["follow_sugguestion"] = suggested_follower_query_arry[:4]
        context['trending']= Post.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')[:6]
        context['tags']=Tag.objects.all().order_by('timestamp')[:4]
        context['notify']=user_notify.notifications.filter(deleted=False).order_by('-timestamp')[:4]
        context['notify_count'] = user_notify.notifications.filter(actor_object_id=user_notify.id,deleted=False,unread=True).count()
        
        
        return context
    

 
class CloseFriendHomeView(LoginRequiredMixin,TemplateView):
   
    login_url = '/accounts/login/'
    template_name = "profiles/close_friend.html"
   

    def get_context_data(self, *args, **kwargs):
        context = super(CloseFriendHomeView, self).get_context_data(*args, **kwargs)
        request = self.request
        user = request.user.userprofile
        user_notify = User.objects.get(username=self.request.user)
        print(user.follower.all(),"hehhehehe")
        is_following_user_ids = [x.id for x in user.follower.all()]

        following_qs = []
        for follower in user.follower.all():
            if follower in user.close_friends.all():
                qs = Post.objects.filter(username__user=follower).order_by('-create_date')[:2]
                for post in qs:
                    following_qs.append(post)
        # qs = Post.objects.filter(
        #                         username__user__my_close_friends__user=request.user
        #                         ).order_by('-create_date')[:10]

        suggested_follower_query = UserProfile.objects.annotate(num_followers=Count('follower')).order_by('-num_followers')
        print(suggested_follower_query,"ajajsja")
        follower_array = []
        
        suggested_follower_query_arry = []

        for suggestion in suggested_follower_query:
            print(suggestion,"suggestion")
            if user != suggestion:
                suggested_follower_query_arry.append(suggestion)
                print(suggested_follower_query_arry,"suggestion inserted")
            


        for user in user.follower.all():
            print(user,'user')
            try:
                follower = UserProfile.objects.get(user=user)
                print(follower,"got a follower")
            except UserProfile.DoesNotExist:
                pass
            
            if follower in suggested_follower_query_arry:
                print(follower,"follower")
                suggested_follower_query_arry.remove(follower)

        print(suggested_follower_query_arry,"arry follower")
            
        
        context['object_list']= following_qs[:10]
        context["follow_sugguestion"] = suggested_follower_query_arry[:4]
        context['trending']= Post.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')[:6]
        context['tags']=Tag.objects.all().order_by('timestamp')[:4]
        context['notify']=user_notify.notifications.filter(deleted=False).order_by('-timestamp')[:4]
        context['notify_count'] = user_notify.notifications.filter(actor_object_id=user_notify.id,deleted=False,unread=True).count()
        return context

class FollowerView(DetailView):
    template_name = "profiles/follower_detail.html"
    model = UserProfile


    def get_object(self):
    
        username = self.kwargs.get("username")
        if username is None:
            raise Http404
        return get_object_or_404(User, username__iexact=username, is_active=True)

    def get_context_data(self, *args, **kwargs):
        context = super(FollowerView,self).get_context_data(*args, **kwargs)
        user = context['user']
        user_com = User.objects.get(username=user)
        myfollowers = user_com.is_following.all()
        myfollowerings = user_com.userprofile.follower.all()
        followers_Array =[]
        followerings_Array =[]
        
        for target_list in myfollowers:
            user_obj = User.objects.get(username=target_list)

            followers_obj = user_obj.is_following.all()
            print(followers_obj,'name o  ki line')
            followerings_Array.append(followerings_Array)
            print(followers_obj,user_obj)

            followerings_obj = user_obj.userprofile.follower.all()
            followerings_Array.append(followerings_obj)
            print(followerings_obj,user_obj)
        print(followerings_Array,'arry one one one ')
        context['myfollowers_data']= followers_Array
        context['myfollowerings_data']=  myfollowerings 

        user = self.request.user.userprofile
        user_notify = User.objects.get(username=self.request.user)
        context['notify'] = user_notify.notifications.filter(deleted=False).order_by('-timestamp')[:4]
        context["notify_count"] = user_notify.notifications.filter(actor_object_id=user_notify.id,deleted=False,unread=True).count()

         
        return context

class FollowingView(DetailView):
    template_name = "profiles/following_detail.html"
    model = UserProfile


    def get_object(self):
    
        username = self.kwargs.get("username")
        if username is None:
            raise Http404
        return get_object_or_404(User, username__iexact=username, is_active=True)

    def get_context_data(self, *args, **kwargs):
        context = super(FollowingView,self).get_context_data(*args, **kwargs)
        user = context['user']
        user_com = User.objects.get(username=user)
        myfollowers = user_com.is_following.all()
        
        followers_Array =[]
        followerings_Array =[]
        
        for target_list in myfollowers:
            user_obj = User.objects.get(username=target_list)

            followers_obj = user_obj.is_following.all()
            print(followers_obj,'name o  ki line')
            followerings_Array.append(followerings_Array)
            print(followers_obj,user_obj)

            followerings_obj = user_obj.userprofile.follower.all()
            followerings_Array.append(followerings_obj)
            print(followerings_obj,user_obj)
        print(followerings_Array,'arry one one one ')
        context['myfollowers_data']= followers_Array
        context['myfollowerings_data']= followerings_obj 

        user = self.request.user.userprofile
        user_notify = User.objects.get(username=self.request.user)
        context['notify'] = user_notify.notifications.filter(deleted=False).order_by('-timestamp')[:4]
        context["notify_count"] = user_notify.notifications.filter(actor_object_id=user_notify.id,deleted=False,unread=True).count()

         
        return context
        


# Rank portions

class RankView(DetailView):
    model=Rank
    template_name = "profiles/ranks/rank_detail.html"


    def get_object(self):
    
        username = self.kwargs.get("username")
        if username is None:
            raise Http404
        return get_object_or_404(User, username__iexact=username, is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = context['user']
        user_profile = UserProfile.objects.get(user=self.request.user)
        ranks = user_profile.rank.all().order_by('-create_date')
        # ranks = self.request.user.userprofile.rank.all()
        print(ranks,'ahshdjsadk')
        context["ranks"] = ranks
        posts = Post.objects.filter(username=user.userprofile).order_by('-create_date')
        context['posts'] = posts

        user = self.request.user.userprofile
        user_notify = User.objects.get(username=self.request.user)
        context['notify'] = user_notify.notifications.filter(deleted=False).order_by('-timestamp')[:4]
        context["notify_count"] = user_notify.notifications.filter(actor_object_id=user_notify.id,deleted=False,unread=True).count()

        return context
    

