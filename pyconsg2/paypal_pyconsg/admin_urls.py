"""Admin URLs of the paypal_pyconsg app."""
from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',
    url(r'payments/$',
        views.PaymentsAndCheckoutChoicesView.as_view(),
        name='payments_and_choices'),
)
