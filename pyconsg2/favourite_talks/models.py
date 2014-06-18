"""Models for the favourite_talks app."""
from django.db import models


class UserPresentation(models.Model):
    """Hooks up a User with a Presentation."""
    user = models.ForeignKey('auth.User')
    presentation = models.ForeignKey('schedule.Presentation')
