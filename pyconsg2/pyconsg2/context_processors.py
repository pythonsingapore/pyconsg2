"""Useful context processors for the pyconsg2 project."""
from django.conf import settings
from symposion.conference.models import Conference


def pyconsg_context_processor(request):
    conference = Conference.objects.all()
    if conference.count():
        conference = conference[0]
    return {
        'conference': conference,
        'BASE_URL': settings.BASE_URL,
    }
