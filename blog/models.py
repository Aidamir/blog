from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify

User = get_user_model()

class Blog(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    content = models.TextField(null=True,blank=True)
    # def get_absolute_url(self):
    #     return reverse('blog', args=[slugify(self.user.username)])
    class Meta:
        app_label = 'blog'


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    content = models.TextField();
    created = models.DateTimeField(auto_now_add=True)
    # def get_absolute_url(self):
    #     return reverse('post', args=[slugify(self.user.username), self.id])
    class Meta:
        app_label = 'blog'

class Read(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey("blog.Post", on_delete=models.CASCADE)
    class Meta:
        app_label = 'blog'


class Follow(models.Model):
    blogger = models.ForeignKey(User, verbose_name="Blogger", on_delete=models.CASCADE, related_name="blogger")
    follower = models.ForeignKey(User, verbose_name="Follower", on_delete=models.CASCADE, related_name="follower")
    class Meta:
        app_label = 'blog'
        unique_together = ('blogger', 'follower')

