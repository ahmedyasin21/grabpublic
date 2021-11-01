from django.shortcuts import render
from posts.models import Post
from blogs.models import Blog
# Create your views here.
from .models import Tag
from django.contrib.auth.models import User
from django.views.generic import ListView,DetailView


class TagListView(ListView):
    model = Tag
    template_name = "tags/tags_list.html"

    def get_queryset(self):
        return Tag.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user.userprofile
        user_notify = User.objects.get(username=self.request.user)
        context["notify"] = user_notify.notifications.filter(deleted=False).order_by('-timestamp')[:4]
        context["notify_count"] = user_notify.notifications.filter(actor_object_id=user_notify.id,deleted=False,unread=True).count()
        return context
    

class TagDetailPostView(DetailView):
    model = Tag
    template_name = "tags/tag_detail_post.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["postlist"] = Post.objects.filter(tag__title=self.object.title)[:15]

        user = self.request.user.userprofile
        user_notify = User.objects.get(username=self.request.user)
        context["notify"] = user_notify.notifications.filter(deleted=False).order_by('-timestamp')[:4]
        context["notify_count"] = user_notify.notifications.filter(actor_object_id=user_notify.id,deleted=False,unread=True).count()
        return context

class TagDetailBlogView(DetailView):
    model = Tag
    template_name = "tags/tag_detail_blog.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["header_bloglist"] = Blog.objects.filter(tag__title=self.object.title)[:6]

        user = self.request.user.userprofile
        user_notify = User.objects.get(username=self.request.user)
        context["notify"] = user_notify.notifications.filter(deleted=False).order_by('-timestamp')[:4]
        context["notify_count"] = user_notify.notifications.filter(actor_object_id=user_notify.id,deleted=False,unread=True).count()
        return context

     
    
