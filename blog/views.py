from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.base import RedirectView
from blog.models import *


@method_decorator(login_required, name='dispatch')
class Posts(ListView):
    template_name = "Posts.html"
    model = Post
    paginate_by = 10
    title = "Recent posts"

    def get(self, request, *args, **kwargs):
        if not self.kwargs.get('slug') and not request.user.follower.count():
            return HttpResponseRedirect(reverse('authors'))
        return super(Posts, self).get(request, *args, **kwargs)

    def get_queryset(self):
        if self.kwargs.get('slug'):
            self.title = 'Posts by ' + (
                'You' if self.request.user.username == self.kwargs.get('slug') else self.kwargs.get('slug'))
            return super(Posts, self).get_queryset().filter(user__username=self.kwargs.get('slug')).order_by('-created')
        return super(Posts, self).get_queryset().filter(user__blogger__follower=self.request.user).exclude(
            user=self.request.user).order_by('-created')


@method_decorator(login_required, name='dispatch')
class Authors(ListView):
    template_name = "Authors.html"
    model = User
    paginate_by = 10
    title = "Authors"

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
    title = "Create post"

    def get_form_class(self):
        form = super(CreatePost, self).get_form_class()
        for field in form.base_fields:
            form.base_fields[field].widget.attrs['class'] = 'form-control'
        return form

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CreatePost, self).form_valid(form)


class RedirectTo(RedirectView):
    def get(self, request, *args, **kwargs):
        self.url = kwargs['to']
        return super(RedirectTo, self).get(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class FollowBlog(RedirectTo):
    def get(self, request, *args, **kwargs):
        try:
            blogger = User.objects.get(username=kwargs['slug'])
        except ObjectDoesNotExist:
            return super(FollowBlog, self).get(request, *args, **kwargs)
        Follow.objects.update_or_create(blogger=blogger, follower=request.user)
        return super(FollowBlog, self).get(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class UnFollowBlog(RedirectTo):
    def get(self, request, *args, **kwargs):
        request.user.follower.filter(blogger__username=kwargs['slug']).delete()
        return super(UnFollowBlog, self).get(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class MarkRead(RedirectTo):
    def get(self, request, *args, **kwargs):
        try:
            post = Post.objects.get(id=kwargs['pk'])
        except ObjectDoesNotExist:
            return super(MarkRead, self).get(request, *args, **kwargs)
        post.mark_read(request.user)
        return super(MarkRead, self).get(request, *args, **kwargs)
