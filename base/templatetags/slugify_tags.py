from django import template
from django.utils.text import slugify

register = template.Library()

@register.filter
def slugify_filter(value):
    return slugify(value,allow_unicode=True)
