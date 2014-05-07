"""Templatetags for the pyconsg2 project."""
from django import template

from cms.models.static_placeholder import StaticPlaceholder


register = template.Library()


@register.assignment_tag
def inspect(obj):
    import ipdb
    ipdb.set_trace()
    return obj


@register.assignment_tag
def get_static_placeholders():
    return StaticPlaceholder.objects.all()
