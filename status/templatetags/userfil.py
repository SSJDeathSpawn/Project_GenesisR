from django import template

register = template.Library()

@register.filter
def get_post_if_liked_by_user(user, post):
    return user.post_liked.filter(pk__iexact=post.pk)