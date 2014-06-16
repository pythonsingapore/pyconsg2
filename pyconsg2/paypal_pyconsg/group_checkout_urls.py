"""The urls for the ``paypal_express_checkout`` app."""
from django.conf.urls import patterns, url

from paypal_express_checkout.views import SetExpressCheckoutView

from . import forms


urlpatterns = patterns(
    '',
    url(
        r'^$',
        SetExpressCheckoutView.as_view(
            form_class=forms.PyconsgGroupSetExpressCheckoutForm,
            template_name='paypal_express_checkout/group_set_checkout.html'),
        name='paypal_group_checkout'
    ),
    url(
        r'^early/$',
        SetExpressCheckoutView.as_view(
            form_class=forms.PyconsgGroupEarlyBirdSetExpressCheckoutForm,
            template_name='paypal_express_checkout/group_set_checkout.html'),
        name='paypal_group_checkout'
    ),
)
