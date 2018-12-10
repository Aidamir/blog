from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.base import View, RedirectView
from blog.models import *
# Create your views here.

class Posts(ListView):
    model = Post

class Authors(ListView):
    template_name = "Authors.html"
    model = User

class CreatePost(CreateView):
    model = Post

class Follow(RedirectView):
    def get(self, request, *args, **kwargs):
        return super(Follow,self).get(request,*args, **kwargs)