"""Templatetags for the favourite_talks app."""
from django import template

from .. import models


register = template.Library()


@register.assignment_tag
def is_favourite(user, presentation):
    """Returns ``True`` if the given presentation is favourited by the user."""
    favourites = models.UserPresentation.objects.filter(
        user=user, presentation=presentation)
    if favourites:
        return True
    return False
