from django import template

register = template.Library()


@register.filter()
def is_follower_of(user, blogger):
    return user.follower.filter(blogger=blogger).exists()


@register.filter()
def is_read(post, user):
    return post.read.filter(follower=user.id).exists()


@register.filter()
def base_url_for_pagination(path, view):
    path = path if path[-1:] != '/' else path[:-1]
    if view.kwargs.get('page'):
        path = '/'.join(path.split('/')[:-1])
    return path

    # return path[:path.find('page') if path.find('page') > 0 else None ]
