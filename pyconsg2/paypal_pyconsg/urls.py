"""Main urls.py of the pyconsg project."""
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import direct_to_template

from .views import CheckoutChoicesView


urlpatterns = patterns(
    '',
    url(r'^$',
        CheckoutChoicesView.as_view(),
        name='checkout_choices'),
)
