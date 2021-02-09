from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from .forms import PostForm,CommentForm
from .models import Post, Comment
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



class PostListView(ListView):
    model = Post
    context_object_name = 'post_list' 
    template_name = 'test.html'
    paginate_by = 3

    def get_queryset(self):
        return Post.objects.filter(create_date__lte=timezone.now()).order_by('-create_date')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['follow_sugguestion']=UserProfile.objects.annotate(num_followers=Count('follower')).order_by('-num_followers')[:4]
        context["trending"] = Post.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')[:14]
        return context
    

class PostDetailView(DetailView):
    model = Post
    template_name = 'posts/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
      
        owner=False
        if self.request.user == post.username.user:
            owner = True
        context["owner"] = owner
        return context


# POst detail by function base view for comment testing

def single_post(request ,*args, **kwargs):
    slug=kwargs.get('slug')
    print(slug,'slug')
    pk=kwargs.get('pk')
    print(pk,'pk')
    post = get_object_or_404(Post,pk=pk,slug=slug)
    allcomments = post.comments.filter(status=True)
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
    
    comment_form = CommentForm()
    return render(
                request,
                 'posts/post_test.html',
                    { 'post': post,
                    #   'comments':  user_comment,
                    #   'comments': comments, 
                      'comment_form': comment_form,
                      'allcomments': allcomments,
                    }
                 )


def final_post(request ,*args, **kwargs):
    slug=kwargs.get('slug')
    print(slug,'slug')
    pk=kwargs.get('pk')
    print(pk,'pk')
    post = get_object_or_404(Post,pk=pk,slug=slug)
    allcomments = post.comments.filter(status=True)
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
    return render(
                request,
                 'posts/final_post.html',
                    { 'post': post,
                    #   'comments':  user_comment,
                    #   'comments': comments, 
                      'comment_form': comment_form,
                      'allcomments': allcomments,
                    }
                 )


def addcomment(request):

    post_id = request.POST.get('post_id')
    print(post_id,' hahahha')
    post_slug = request.POST.get('post_slug')
    post = get_object_or_404(Post,pk=post_id,slug=post_slug)
  
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
                user_comment.post = post
                user_comment.save()
                return JsonResponse({'result2': result, 'user': user})




class PostCreateView(LoginRequiredMixin,CreateView):
    login_url = '/accounts/login/'
    redirect_field_name='posts/post_detail.html'
    template_name = 'posts/post_form_final.html'
    form_class = PostForm
    model = Post 
    
    def form_valid(self, form):
        user_post = form.save(commit=False)
        user_post.username = self.request.user.userprofile
        user_post.save()
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    login_url = '/accounts/login/'
    redirect_field_name='posts/post_detail.html'
    form_class = PostForm
    model = Post

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.username.user:
            return True
        return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    login_url = '/accounts/login/'
    model = Post
    success_url = reverse_lazy('posts:post_list')

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.username.user:
            return True
        return False




class PostLikeToggle(LoginRequiredMixin,RedirectView):
    login_url = '/accounts/login/'
    
    def get_redirect_url(self, *args, **kwargs):
        slug=self.kwargs.get('slug')
        print(slug,'slug')
        pk=self.kwargs.get('pk')
        print(pk,'pk')
        obj =get_object_or_404(Post,pk=pk,slug=slug)
        print(obj,'post')
       
        user=self.request.user
        if user.is_authenticated:
            if user in obj.likes.all():
                obj.likes.remove(user)
            else:
                obj.likes.add(user)
        return f'/posts/{pk}/{slug}'





def like(request):
    if request.POST.get('action') == 'post':
        result = ''
        liked = False
        id = int(request.POST.get('postid'))
        post = get_object_or_404(Post, id=id)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
            result = post.likes.count()
            post.save()
            
        else:
            post.likes.add(request.user)
            actor = request.user
            print(actor,'hey')
            recipient_user = post.username
            recipient_obj = User.objects.get(username=recipient_user)
            print(recipient_user,'heybro')
            notify.send(actor, recipient=recipient_obj, verb=f'Like Your post with title "{post.title}"')
            result = post.likes.count()
            liked = True
            post.save()

        return JsonResponse({'result': result,'liked':liked })

def featured(request):
    if request.POST.get('action') == 'post':
        result = ''
        id = int(request.POST.get('postid'))
        post = get_object_or_404(Post, id=id)
        if post.features.filter(id=request.user.id).exists():
            post.features.remove(request.user)
            result = post.features.count()
            post.save()
        else:
            post.features.add(request.user)
            result = post.features.count()
            post.save()
        return JsonResponse({'result1': result})







# class PostLikeApiToggle(APIView):
  
#     authentication_classes = [authentication.TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, format=None):
#         slug=self.kwargs.get('slug')
#         pk=self.kwargs.get('pk')
#         obj =get_object_or_404(Post,pk=pk,slug=slug)
#         user=request.user
#         print(user,'jh')
#         liked= False
#         updated = False
#         if user.is_authenticated:
#             if user in obj.likes.all():
#                 liked= False
#                 obj.likes.remove(user)
#             else:
#                 liked= True
#                 obj.likes.add(user)
#             updated = False
#         data = {
#             "updated": updated,
#             "liked": liked
#         }
#         return Response(data)
    
    



class CommentCreateView(LoginRequiredMixin, CreateView):
    
    model = Comment
    form_class = CommentForm
    template_name = "posts/snippets/comment_form.html"

    def form_valid(self, form,*args, **kwargs):
        form.instance.post_id = self.kwargs['pk']
        # form.instance.post_slug = kwargs['slug']
        form.instance.author = self.request.user
        return super().form_valid(form)


class CommentDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Comment
    success_url = reverse_lazy('posts:post_list')

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.username.user:
            return True
        return False


# class UserPostListView(ListView):
#     model = Post
#     context_object_name = 'userpost_list' 
#     template_name = 'profiles/userpost_list.html'
    
#     def get_queryset(self):
#         user = get_object_or_404(User, username = self.kwargs.get('username'))
#         return Post.objects.filter(username = user).order_by('-create_date')

