from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.base import View, RedirectView
from blog.models import *
# Create your views here.

class Posts(ListView):
    template_name = "Posts.html"
    model = Post

class Authors(ListView):
    template_name = "Authors.html"
    model = User

class DetailPost(DetailView):
    template_name = "DetailPost.html"
    model = Post

class CreatePost(CreateView):
    template_name = "CreatePost.html"
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreatePost, self).form_valid(form)


class Follow(RedirectView):
    def get(self, request, *args, **kwargs):
        self.url = kwargs['to']
        return super(Follow,self).get(request, *args, **kwargs)