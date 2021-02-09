from django.shortcuts import render,redirect,get_object_or_404
from .models import UserProfile
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
    refirect_field_name ='profiles:final_detail'
    form_class = UserUpdateForm
    model = UserProfile

    def get_object(self, *args, **kwargs):
        return self.request.user.userprofile
    
    def get_context_data(self, *args, **kwargs):
        context = super(ProfileUpdateView, self).get_context_data(*args, **kwargs)
        update_form = UserUpdateForm(instance = self.request.user.userprofile)
        context['form']=update_form
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
            profile_, is_following = UserProfile.objects.toggle_follow(request.user, request.user.id ,username_to_toggle)
            return JsonResponse({'result': is_following, })


    


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
        return context

class FolloweHomeView(LoginRequiredMixin,View):
   
    login_url = '/accounts/login/'
    def get(self, request, *args, **kwargs):
    

        user = request.user.userprofile
        user_notify = User.objects.get(username=self.request.user)
        print(user.follower.all())
        is_following_user_ids = [x.id for x in user.follower.all()]
        qs = Post.objects.filter(
                                username__user__is_following__user=request.user
                                ).order_by('-create_date')[:10]
        return render(request, "profiles/follower_home_feed.html", {'object_list': qs,
        'follow_sugguestion':UserProfile.objects.annotate(num_followers=Count('follower')).order_by('-num_followers')[:4],
        'trending': Post.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')[:6],
        'tags':Tag.objects.all().order_by('timestamp')[:4],
        'notify':user_notify.notifications.all().order_by('-timestamp')[:4]
    })

 
class CloseFriendHomeView(LoginRequiredMixin,View):
   
    login_url = '/accounts/login/'
    

    def get(self, request, *args, **kwargs):
    

        user = request.user.userprofile
        print(user.follower.all())
        is_following_user_ids = [x.id for x in user.follower.all()]
        qs = Post.objects.filter(
                                username__user__my_close_friends__user=request.user
                                ).order_by('-create_date')[:10]
        return render(request, "profiles/close_friend.html", {'object_list': qs,
        'follow_sugguestion':UserProfile.objects.annotate(num_followers=Count('follower')).order_by('-num_followers')[:10],
        'trending': Post.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')[:6],
        'tags':Tag.objects.all().order_by('-timestamp')[:6]
    })

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
         
        return context
        



    # def get(self, request, *args, **kwargs):
    #     profile_ = UserProfile.objects.get(user=request.user)
    #     users = [user for user in profile_.follower.all()]
    #     posts = []
    #     qs=None

    #     for u in users:
    #         p = UserProfile.objects.get(user=u)
    #         p_post = p.post_set.all()
    #         posts.append(p_post)
        
    #     if len(posts)>0:
    #         qs = sorted(chain(*posts), reverse = True, key=lambda obj:obj.create_date)
        
    #     return render(request, "profiles/follower_home_feed.html", {'profile': profile_,'object_list':qs})

   
    # def get_context_data(self, *args, **kwargs):
    #         context = super().get_context_data(*args,**kwargs) 
    #         print(self.object.user,'view profile')
    #         print(self.request.user.userprofile.follower.all(),'my profile')
    #         is_following = False
    #         if self.object.user in self.request.user.userprofile.follower.all():
    #             is_following = True
    #         context["is_following"] = is_following
    #         return context

    # def get_object(self, *args, **kwargs):
    #     pk = self.kwargs.get('pk')
    #     view_profile = UserProfile.objects.get(pk=pk)
    #     return view_profile

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     view_profile = self.get_object()
    #     print(view_profile.user,'view profile')
    #     my_profile = UserProfile.objects.get(user=self.request.user)
    #     print(my_profile,'my profile')
    #     is_following = False
    #     if view_profile.user in my_profile.follower.all():
    #         is_following=True

    #     context["is_following"] = is_following
    #     return context
    
    

    # def get_queryset(self,*args, **kwargs):
    #     userss = get_object_or_404(User, username=self.kwargs.get('username'))
    #     return UserProfile.objects.filter(user=userss).order_by('-create_date')






        
        



# @login_required
# def userprofile(request):
#     # puplated field with the user data
#     if request.method == 'POST':
#         u_form = UserUpdateForm(request.POST,instance=request.user)
#         p_form = UserProfileForm(request.POST,request.FILES,instance=request.user.userprofile)
#     # now check if both forms are valid or not 
#         if u_form.is_valid() and p_form.is_valid():
#             u_form.save()
#             p_form.save()
#     #after all the process you need to tell user if all changes are saved than use masseges
#             messages.success(request,f'Your account has been updated!')
#             return redirect('profiles:home')
#     else :
#         u_form = UserUpdateForm(instance=request.user)
#         p_form = UserProfileForm(instance=request.user.userprofile)
    
#     def ger_object(self,*args, **kwargs):
#         request = self.request
#         slug = self.kwargs.get('slug')
#         try:
#             instance = UserProfile.objects.get(slug=slug,active = True)
#         except UserProfile.DoesNotExists:
#             raise Http404("Not found")
#         except UserProfile.MultipleObjectsReturned:
#             qs = UserProfile.objects.filter(slug = slug,  active=True)
#             instance = qs.first()
#         except:
#             raise Http404('Uhmm')
#         return instance   


#     context ={
#         'u_form' :u_form,
#         'p_form':p_form
#     }
#     return render(request,"profiles/userprofile.html",context)


    



# class UserProfileCreateView(LoginRequiredMixin,CreateView):
#     form_class = UserProfileForm()
#     model = UserProfile
#     form_class = UserUpdateForm
#     model = get_user_model()
    
#     queryset = User.objects.all()
#     redirect_field_name='profiles/userprofile.html'
    
    

    # def form_valid(self,p_form):
    #     self.object = form.save(commit = False)
    #     self.object.user = self.request.user
    #     self.object.save()
    #     return super().form_valid(p_form)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["form"] = form_class
    #     return context
    




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
        return context
    

