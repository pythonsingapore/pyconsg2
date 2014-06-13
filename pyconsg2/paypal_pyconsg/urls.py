"""URLs of the paypal_pyconsg app."""
from django.conf.urls import patterns, url

from .views import CheckoutChoicesView


urlpatterns = patterns(
    '',
    url(r'$',
        CheckoutChoicesView.as_view(),
        name='checkout_choices'),
)
