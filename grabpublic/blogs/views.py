from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from .forms import BlogForm
from blogs.forms import CommentForm
from blogs.models import Comment
from .models import Blog
from django.contrib.auth.models import User
from django.views.generic import CreateView,UpdateView,DetailView,DeleteView,ListView,TemplateView,RedirectView
from django.urls import reverse_lazy,reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.db.models import Count
from profiles.models import UserProfile
from notifications.signals import notify

class BlogListView(ListView):
    model = Blog
    context_object_name = 'blod_list' 
    template_name = 'blogs/blog_list.html'
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        user = request.user.userprofile
        user_notify = User.objects.get(username=self.request.user)
        return render(request, "blogs/blog_list.html", {'notify':user_notify.notifications.filter(deleted=False).order_by('-timestamp')[:4]})


    def get_queryset(self):
        return Blog.objects.filter(create_date__lte=timezone.now()).order_by('-create_date')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['follow_sugguestion']=UserProfile.objects.annotate(num_followers=Count('follower')).order_by('-num_followers')[:4]
        context["trending"] = Blog.objects.annotate(num_likes=Count('fans')).order_by('-num_fans')[:14]
        return context
    

class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blogs/blog_detail.html'

    def get(self, request, *args, **kwargs):
        user = request.user.userprofile
        user_notify = User.objects.get(username=self.request.user)
        return render(request, "blogs/blog_detail.html", {'notify':user_notify.notifications.filter(deleted=False).order_by('-timestamp')[:4]})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = self.get_object()
      
        owner=False
        if self.request.user == blog.username.user:
            owner = True
        context["owner"] = owner
        return context


# POst detail by function base view for comment testing

def single_blog(request ,*args, **kwargs):
    slug=kwargs.get('slug')
    print(slug,'slug')
    pk=kwargs.get('pk')
    print(pk,'pk')
    blog = get_object_or_404(Blog,pk=pk,slug=slug)
    allcomments = blog.blog_comments.filter(status=True)
    page = request.GET.get('page', 1)

    paginator = Paginator(allcomments, 4)
    try:
        allcomments = paginator.page(page)
    except PageNotAnInteger:
        allcomments = paginator.page(1)
    except EmptyPage:
        allcomments = paginator.page(paginator.num_pages)
    # user_comment = None

    # if request.method =='POST':
    #     comment_form = CommentForm(request.POST)
    # if comment_form.is_valid():
    #         user_comment = comment_form.save(commit=False)
            # user_comment.post = post
    #         user_comment.save()
    #         return HttpResponseRedirect(f'/posts/test/{pk}/{slug}')
    # else:
    user_notify = User.objects.get(username=request.user)
    comment_form = CommentForm()
    return render(
                request,
                 'blogs/blog_detail.html',
                    { 'blog': blog,
                    #   'comments':  user_comment,
                    #   'comments': comments, 
                      'comment_form': comment_form,
                      'allcomments': allcomments,
                      'notify':user_notify.notifications.filter(deleted=False).order_by('-timestamp')[:4],
                      'notify_count':user_notify.notifications.filter(actor_object_id=user_notify.id,deleted=False,unread=True).count()
                    }
                 )


def final_blog(request ,*args, **kwargs):
    slug=kwargs.get('slug')
    print(slug,'slug')
    pk=kwargs.get('pk')
    print(pk,'pk')
    blog = get_object_or_404(Blog,pk=pk,slug=slug)
    allcomments = blog.blog_comments.filter(status=True)
    page = request.GET.get('page', 1)

    # paginator = Paginator(allcomments, 4)
    # try:
    #     allcomments = paginator.page(page)
    # except PageNotAnInteger:
    #     allcomments = paginator.page(1)
    # except EmptyPage:
    #     allcomments = paginator.page(paginator.num_pages)
    # user_comment = None

    # if request.method =='POST':
    #     comment_form = CommentForm(request.POST)
    # if comment_form.is_valid():
    #         user_comment = comment_form.save(commit=False)
            # user_comment.post = post
    #         user_comment.save()
    #         return HttpResponseRedirect(f'/posts/test/{pk}/{slug}')
    # else:
    
    comment_form = CommentForm()
    user = request.user.userprofile
    user_notify = User.objects.get(username=request.user)
    return render(
                request,
                 'blogs/final_blog.html',
                    { 'blog': blog,
                    #   'comments':  user_comment,
                    #   'comments': comments, 
                      'comment_form': comment_form,
                      'allcomments': allcomments,
                      'notify':user_notify.notifications.filter(deleted=False).order_by('-timestamp')[:4],
                      'notify_count':user_notify.notifications.filter(actor_object_id=user_notify.id,deleted=False,unread=True).count()
                    }
                 )


def addcomment(request):

    blog_id = request.POST.get('blog_id')
    print(blog_id,' hahahha')
    blog_slug = request.POST.get('blog_slug')
    blog = get_object_or_404(Blog,pk=blog_id,slug=blog_slug)
  
    if request.method == 'POST':
        print('hello')
        if request.POST.get('action') == 'delete':
            id = request.POST.get('nodeid')
            print(id,'node ids')
            c = Comment.objects.get(id=id)
            c.delete()
            return JsonResponse({'remove': id})
        else:
            comment_form = CommentForm(request.POST)
            print(comment_form)
            if comment_form.is_valid():
                user_comment = comment_form.save(commit=False)
                result = comment_form.cleaned_data.get('body')
                user = request.user.username
                print(user,'userserser')
                print(result,'rseskjsaks')
                user_comment.author = request.user
                user_comment.blog = blog
                user_comment.save()
                return JsonResponse({'result2': result, 'user': user})




class BlogCreateView(LoginRequiredMixin,CreateView):
    login_url = '/accounts/login/'
    redirect_field_name='blogs/blog_detail.html'
    form_class = BlogForm
    model = Blog 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user.userprofile
        user_notify = User.objects.get(username=user)
        context["notify"] = user_notify.notifications.filter(deleted=False).order_by('-timestamp')[:4]
        context["notify_count"] = user_notify.notifications.filter(actor_object_id=user_notify.id,deleted=False,unread=True).count()
        return context
    
    
    def form_valid(self, form):
        user_blog = form.save(commit=False)
        user_blog.username = self.request.user.userprofile
        user_blog.save()
        return super().form_valid(form)

class BlogUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    login_url = '/accounts/login/'
    redirect_field_name='blogs/blog_detail.html'
    form_class = BlogForm
    model = Blog

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user.userprofile
        user_notify = User.objects.get(username=user)
        context["notify"] = user_notify.notifications.filter(deleted=False).order_by('-timestamp')[:4]
        context["notify_count"] = user_notify.notifications.filter(actor_object_id=user_notify.id,deleted=False,unread=True).count()
        return context

    def test_func(self):
        blog = self.get_object()
        if self.request.user == blog.username.user:
            return True
        return False

class BlogDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    login_url = '/accounts/login/'
    model = Blog
    success_url = reverse_lazy('blogs:blog_draft_list')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user.userprofile
        user_notify = User.objects.get(username=user)
        context["notify"] = user_notify.notifications.filter(deleted=False).order_by('-timestamp')[:4]
        context["notify_count"] = user_notify.notifications.filter(actor_object_id=user_notify.id,deleted=False,unread=True).count()
        return context

        
    def test_func(self):
        blog = self.get_object()
        if self.request.user == blog.username.user:
            return True
        return False
    



def fan(request):
    if request.POST.get('action') == 'post':
        result = ''
        liked = False
        id = int(request.POST.get('blogid'))
        blog = get_object_or_404(Blog, id=id)
        if blog.fans.filter(id=request.user.id).exists():
            blog.fans.remove(request.user)
            result = blog.fans.count()
            blog.save()
            
        else:
            blog.fans.add(request.user)
            actor = request.user
            print(actor,'hey')
            recipient_user = blog.username
            recipient_obj = User.objects.get(username=recipient_user)
            print(recipient_user,'heybro')
            notify.send(actor, recipient=recipient_obj, verb=f'Like Your blog with title "{blog.title}"')
            result = blog.fans.count()
            liked = True
            blog.save()

        return JsonResponse({'result': result,'liked':liked })

def favorites(request):
    if request.POST.get('action') == 'post':
        result = ''
        id = int(request.POST.get('blogid'))
        blog = get_object_or_404(Blog, id=id)
        if blog.favorites.filter(id=request.user.id).exists():
            blog.features.remove(request.user)
            result = blog.features.count()
            blog.save()
        else:
            blog.favorites.add(request.user)
            result = blog.favorites.count()
            blog.save()
        return JsonResponse({'result1': result})

class DraftListView(ListView):
    model = Blog

    
    def get(self, request, *args, **kwargs):
        user = request.user.userprofile
        user_notify = User.objects.get(username=self.request.user)
        notify_count = user_notify.notifications.filter(actor_object_id=user_notify.id,deleted=False,unread=True).count()
        return render(request, "blogs/blog_draft.html", {'notify':user_notify.notifications.filter(deleted=False).order_by('-timestamp')[:4],'notify_count':notify_count})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blogs = Blog.objects.filter(username=self.request.user.userprofile).order_by('-create_date')
        context["object_list"] = blogs
        return context

class PublishedListView(ListView):
    model = Blog


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blogs = Blog.objects.filter(username=self.request.user.userprofile).order_by('-create_date')
        blog=[]
        for b in blogs:
            if b.published:
                blog.append(b)
            else:
                blog.append('no published')
        context["object_list"] = blogs

        user = self.request.user.userprofile
        user_notify = User.objects.get(username=self.request.user)
        context["notify"] = user_notify.notifications.filter(deleted=False).order_by('-timestamp')[:4]
        context["notify_count"] = user_notify.notifications.filter(actor_object_id=user_notify.id,deleted=False,unread=True).count()
        return context
    




def blog_publish(request,pk,slug):
    blog = get_object_or_404(Blog,pk=pk,slug=slug)
    blog.publish()
    return redirect('blogs:blog_detail_final',pk=pk,slug=slug)




