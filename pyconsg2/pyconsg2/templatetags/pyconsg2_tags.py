"""Templatetags for the pyconsg2 project."""
from django import template


register = template.Library()


@register.simple_tag
def inspect(obj):
    import ipdb; ipdb.set_trace() # BREAKPOINT
    return obj
