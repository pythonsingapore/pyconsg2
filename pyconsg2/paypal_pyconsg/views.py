"""Views for the ``paypal_pyconsg`` app."""
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.generic import FormView, TemplateView

from paypal_express_checkout.models import PaymentTransaction

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


class PaymentsAndCheckoutChoicesView(TemplateView):
    template_name = 'paypal_pyconsg/payments_and_checkout_choices_view.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return super(PaymentsAndCheckoutChoicesView, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(PaymentsAndCheckoutChoicesView, self).get_context_data(
            **kwargs)
        completed_transactions = PaymentTransaction.objects.filter(
            status='Completed').prefetch_related('checkout_choices')
        ctx.update({
            'transactions': completed_transactions,
        })
        return ctx
