import os

from django import template

register = template.Library()


@register.filter
def extension(value):
    return os.path.splitext(value.name)[1][1:]  # e.g., "pdf"
