from django import template

register = template.Library()

# @register.assignment_tag()
# def is_follower_of(user, blogger):
#     return user.follower.filter(blogger=blogger).exist()


@register.filter()
def is_follower_of(user, blogger):
    return user.follower.filter(blogger=blogger).exists()
