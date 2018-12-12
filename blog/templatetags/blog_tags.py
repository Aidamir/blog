from django import template

register = template.Library()


@register.filter()
def is_follower_of(user, blogger):
    return user.follower.filter(blogger=blogger).exists()


@register.filter()
def is_read(post, user):
    return post.read.filter(follower=user.id).exists()
