"""Views for the ``paypal_pyconsg`` app."""
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import Http404
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import FormView, TemplateView

from paypal_express_checkout.models import PaymentTransaction

from . import models
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


class AttendeeOverviewView(TemplateView):
    template_name = 'paypal_pyconsg/attendee_overview_view.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return super(AttendeeOverviewView, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(AttendeeOverviewView, self).get_context_data(
            **kwargs)
        choices = models.CheckoutChoices.objects.filter(
            transaction__status='Completed')
        conference_tickets = choices.filter(has_conference_ticket=True)
        conference_tickets_students = conference_tickets.filter(
            is_student=True)
        tutorial_morning_tickets = choices.filter(
            tutorial_morning__isnull=False)
        tutorial_morning_tickets_students = tutorial_morning_tickets.filter(
            is_student=True)
        tutorial_afternoon_tickets = choices.filter(
            tutorial_afternoon__isnull=False)
        tutorial_afternoon_tickets_students = \
            tutorial_afternoon_tickets.filter(is_student=True)
        tutorial_total_tickets = tutorial_morning_tickets.count() + \
            tutorial_afternoon_tickets.count()
        tutorial_total_tickets_students = \
            tutorial_morning_tickets_students.count() + \
            tutorial_afternoon_tickets_students.count()

        tshirt_sizes = choices.values('tshirt_size').annotate(
            size_count=Count('tshirt_size')).order_by('size_count')
        food_preferences = choices.values('food_choice').annotate(
            choice_count=Count('food_choice')).order_by('choice_count')
        for pref in food_preferences:
            if pref['food_choice'] is None:
                pref['display_value'] = 'n/a'
            else:
                for choice in models.FOOD_CHOICES:
                    if choice[0] == pref['food_choice']:
                        pref['display_value'] = choice[1]
        tutorials_morning = choices.filter(
            tutorial_morning__isnull=False).values(
            'tutorial_morning__title').annotate(
            tut_count=Count('tutorial_morning__title')).order_by('tut_count')
        tutorials_afternoon = choices.filter(
            tutorial_afternoon__isnull=False).values(
            'tutorial_afternoon__title').annotate(
            tut_count=Count('tutorial_afternoon__title')).order_by(
            'tut_count')
        ctx.update({
            'conference_tickets': conference_tickets.count(),
            'conference_tickets_students': conference_tickets_students.count(),
            'tutorial_morning_tickets': tutorial_morning_tickets.count(),
            'tutorial_morning_tickets_students': tutorial_morning_tickets_students.count(),  # NOQA
            'tutorial_afternoon_tickets': tutorial_afternoon_tickets.count(),
            'tutorial_afternoon_tickets_students': tutorial_afternoon_tickets_students.count(),  # NOQA
            'tutorial_total_tickets': tutorial_total_tickets,
            'tutorial_total_tickets_students': tutorial_total_tickets_students,
            'tshirt_sizes': tshirt_sizes,
            'food_preferences': food_preferences,
            'tutorials_morning': tutorials_morning,
            'tutorials_afternoon': tutorials_afternoon,
        })
        return ctx


class ConferenceReceptionView(TemplateView):
    template_name = 'paypal_pyconsg/conference_reception_view.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return super(ConferenceReceptionView, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super(ConferenceReceptionView, self).get_context_data(
            **kwargs)
        choices = models.CheckoutChoices.objects.filter(
            transaction__status='Completed').select_related(
            'user', 'user__speaker_profile__presentations', 'transaction',
            'tutorial_morning', 'tutorial_afternoon')
        speakers = choices.filter(
            user__speaker_profile__presentations__isnull=False).distinct()
        missing_speakers = speakers.filter(is_registered=False)
        ctx.update({
            'choices': choices,
            'speakers': speakers,
            'missing_speakers': missing_speakers,
        })
        return ctx

    def post(self, request, *args, **kwargs):
        choice_pk = int(request.POST.get('choice_pk'))
        choice = models.CheckoutChoices.objects.get(pk=choice_pk)
        if 'btn-register' in request.POST:
            register = True
        else:
            register = False
        choice.is_registered = register
        choice.save()
        return redirect('reception')
