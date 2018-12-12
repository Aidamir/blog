from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode
from blog.email_util import send_mass_mail_template
from django.contrib.sites.models import Site


User = get_user_model()

# Dont't know if it is need?
class Blog(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)

    # def get_absolute_url(self):
    #     return reverse('blog', args=[slugify(self.user.username)])

    class Meta:
        app_label = 'blog'


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    content = models.TextField();
    created = models.DateTimeField(auto_now_add=True)
    read = models.ManyToManyField(User, verbose_name="Read by", related_name="readby")

    def get_absolute_url(self):
        #         return reverse('detail', args=[slugify(self.user.username), slugify(unidecode(self.title))])
        return reverse('detail', args=[slugify(self.user.username), self.id])

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.id is None:
            ret = super(self, Post).save(force_insert=force_insert, force_update=force_update, using=using,
                                         update_fields=update_fields)
            try:
                send_mass_mail_template('email/NewPost',
                                        [u.follower for u in self.user.blogger.all()],
                                        "New Post", context={'post': self, 'domain': Site.objects.get_current().domain })
            except Exception:
                pass
            return ret
        return super(Post, self).save(force_insert=force_insert, force_update=force_update, using=using,
                                      update_fields=update_fields)

    class Meta:
        app_label = 'blog'


class Follow(models.Model):
    blogger = models.ForeignKey(User, verbose_name="Blogger", on_delete=models.CASCADE, related_name="blogger")
    follower = models.ForeignKey(User, verbose_name="Follower", on_delete=models.CASCADE, related_name="follower")

    class Meta:
        app_label = 'blog'
        unique_together = ('blogger', 'follower')

    def delete(self, using=None, keep_parents=False):
        # remove all read marks as requested in task definition
        for p in Post.objects.filter(blogger=self.blogger, read=self.follower):
            p.read.remove(self.follower)
        return super(Follow, self).delete(using=using, keep_parents=keep_parents)
