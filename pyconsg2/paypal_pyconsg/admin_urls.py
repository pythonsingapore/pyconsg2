"""Admin URLs of the paypal_pyconsg app."""
from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'attendees/$',
        views.AttendeeOverviewView.as_view(),
        name='attendees_overview'),
    url(r'payments/$',
        views.PaymentsAndCheckoutChoicesView.as_view(),
        name='payments_and_choices'),
)
