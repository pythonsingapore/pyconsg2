"""Forms for the group_registrations app."""
import datetime

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from account.models import EmailAddress
from paypal_express_checkout.models import PaymentTransaction
from symposion.schedule.models import Presentation

from paypal_pyconsg.models import CheckoutChoices, FOOD_CHOICES, TSHIRT_CHOICES


class GroupRegistrationsForm(forms.Form):
    """Form that allows to add a user as part of a group registration."""
    transaction_id = forms.CharField(max_length=128)
    first_name = forms.CharField(max_length=128)
    last_name = forms.CharField(max_length=128)
    email = forms.EmailField(max_length=128)
    is_student = forms.BooleanField(required=False)
    has_conference_ticket = forms.BooleanField(required=False)
    tutorial_morning = forms.ModelChoiceField(
        label=_('Tutorial (morning)'),
        queryset=Presentation.objects.filter(
            proposal_base__kind__slug='tutorial',
            slot__start__lte=datetime.time(13, 0)),
        empty_label='------',
        required=False,
    )
    tutorial_afternoon = forms.ModelChoiceField(
        label=_('Tutorial (afternoon)'),
        queryset=Presentation.objects.filter(
            proposal_base__kind__slug='tutorial',
            slot__start__gt=datetime.time(13, 0)),
        empty_label='------',
        required=False,
    )
    tshirt_size = forms.ChoiceField(
        label=_('T-Shirt size'),
        choices=TSHIRT_CHOICES,
        initial='L',
    )

    food_choice = forms.ChoiceField(
        label=_('Food preference'),
        choices=FOOD_CHOICES,
        initial=None,
        required=False,
    )

    def save(self, *args, **kwargs):
        user = None
        try:
            user = User.objects.get(email=self.cleaned_data.get('email'))
        except User.DoesNotExist:
            pass
        if user is None:
            user = User.objects.create(
                username=self.cleaned_data.get('email'),
                first_name=self.cleaned_data.get('first_name'),
                last_name=self.cleaned_data.get('last_name'),
                email=self.cleaned_data.get('email'),
            )
            user.set_password('start123')
            user.save()

        email = None
        try:
            email = EmailAddress.objects.get(
                email=self.cleaned_data.get('email'))
        except EmailAddress.DoesNotExist:
            pass
        if email is None:
            email = EmailAddress.objects.create(
                user=user,
                email=self.cleaned_data.get('email'),
                verified=True,
                primary=True,
            )
        email.verified = True
        email.save()

        transaction = PaymentTransaction.objects.get(
            transaction_id=self.cleaned_data.get('transaction_id'))

        CheckoutChoices.objects.filter(user=user).delete()
        CheckoutChoices.objects.create(
            user=user,
            transaction=transaction,
            is_student=self.cleaned_data.get('is_student'),
            has_conference_ticket=self.cleaned_data.get(
                'has_conference_ticket'),
            tutorial_morning=self.cleaned_data.get('tutorial_morning'),
            tutorial_afternoon=self.cleaned_data.get('tutorial_afternoon'),
            tshirt_size=self.cleaned_data.get('tshirt_size'),
            food_choice=self.cleaned_data.get('food_choice'),
        )
