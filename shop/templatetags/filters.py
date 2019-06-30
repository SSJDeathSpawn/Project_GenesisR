from django import template
from ..models import *

register = template.Library()

@register.filter
def first_image(item):
    if item.photo_set.all():
        return item.photo_set.all()[0].photo.url
    return None