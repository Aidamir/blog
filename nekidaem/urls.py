"""nekidaem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth.views import LoginView, LogoutView
from blog.views import *


urlpatterns = [
    path('', Posts.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path("accounts/login/", LoginView.as_view(), name='login'),
    path("accounts/logout/", LogoutView.as_view(), name='logout'),
    re_path("^follow/(?P<slug>[0-9a-zA-Z_-]+)/(?P<to>[/0-9a-zA-Z_-]+)$", FollowBlog.as_view(), name="follow"),
    re_path("^unfollow/(?P<slug>[0-9a-zA-Z_-]+)/(?P<to>[/0-9a-zA-Z_-]+)$", UnFollowBlog.as_view(), name="unfollow"),
    re_path("^authors/$", Authors.as_view(), name="authors"),
    re_path("^posts/$", Posts.as_view(), name="posts"),
    re_path("^create/$", CreatePost.as_view(), name="create"),
#    re_path("^([0-9a-zA-Z_-]+)/([0-9a-zA-Z_-]+)$", DetailPost.as_view(), name="detail"),
    re_path("^([0-9a-zA-Z_-]+)/(?P<pk>[0-9]+)$", DetailPost.as_view(), name="detail"),
]

