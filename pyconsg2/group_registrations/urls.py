"""URLs for the group_registrations app."""
from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'$', views.GroupRegistrationsView.as_view(),
        name='group_registrations')
)
