"""Views for the favourite_talks app."""
from django.views.generic import View
from django.shortcuts import redirect

from symposion.schedule.models import Presentation

from . import models


class ToggleFavouriteTalkView(View):
    """Marks a presentation for a user as favourite."""
    def post(self, request, *args, **kwargs):
        presentation_pk = int(request.POST.get('presentation'))
        presentation = Presentation.objects.get(pk=presentation_pk)
        fav, created = models.UserPresentation.objects.get_or_create(
            user=request.user,
            presentation=presentation)
        if not created:
            fav.delete()
        return redirect('/schedule/')
