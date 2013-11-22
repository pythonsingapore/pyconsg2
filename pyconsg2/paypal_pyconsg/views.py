"""Views for the ``paypal_pyconsg`` app."""
from django.views.generic import FormView

from .forms import CheckoutChoicesForm


class CheckoutChoicesView(FormView):
    form_class = CheckoutChoicesForm
    success_url = '/dashboard/'
    template_name = 'paypal_pyconsg/checkout_choices.html'

    def form_valid(self, form):
        form.save()
        return super(CheckoutChoicesView, self).form_valid(form)

    def get_form_kwargs(self):
        kwargs = super(CheckoutChoicesView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user, })
        return kwargs
