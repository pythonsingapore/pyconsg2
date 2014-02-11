"""Templatetags for the pyconsg2 project."""
from django import template


register = template.Library()


@register.assignment_tag
def inspect(obj):
    import ipdb
    ipdb.set_trace()
    return obj
