from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.base import View, RedirectView
from blog.models import *


# Create your views here.
@method_decorator(login_required, name='dispatch')
class Posts(ListView):
    template_name = "Posts.html"
    model = Post

    def get(self, request, *args, **kwargs):
        if not request.user.follower.count():
            return HttpResponseRedirect(reverse('authors'))
        return super(Posts, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return super(Posts, self).get_queryset().filter(user__blogger__follower=self.request.user).exclude(user=self.request.user).order_by('-created')


@method_decorator(login_required, name='dispatch')
class Authors(ListView):
    template_name = "Authors.html"
    model = User

    def get_queryset(self):
        return super(Authors, self).get_queryset().exclude(id=self.request.user.id)


@method_decorator(login_required, name='dispatch')
class DetailPost(DetailView):
    template_name = "DetailPost.html"
    model = Post


@method_decorator(login_required, name='dispatch')
class CreatePost(CreateView):
    template_name = "CreatePost.html"
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreatePost, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class FollowBlog(RedirectView):
    def get(self, request, *args, **kwargs):
        try:
            blogger = User.objects.get(username=kwargs['slug'])
        except ObjectDoesNotExist:
            return super(FollowBlog, self).get(request, *args, **kwargs)
        Follow.objects.update_or_create(blogger=blogger, follower=request.user)
        self.url = kwargs['to']
        return super(FollowBlog, self).get(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class UnFollowBlog(RedirectView):
    def get(self, request, *args, **kwargs):
        request.user.follower.filter(blogger__username=kwargs['slug']).delete()
        self.url = kwargs['to']
        return super(UnFollowBlog, self).get(request, *args, **kwargs)
