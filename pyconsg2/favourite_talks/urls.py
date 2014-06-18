"""URLs for the favourite_talks app."""
from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'toggle/$',
        views.ToggleFavouriteTalkView.as_view(),
        name='toggle_favourite_view'),
)
