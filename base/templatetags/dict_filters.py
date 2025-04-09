from django import template

register = template.Library()


@register.filter
def dictkey(d: dict, key):
    return d.get(key)
