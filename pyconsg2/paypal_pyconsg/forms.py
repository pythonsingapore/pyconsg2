"""
Forms for the ``paypal_express_checkout`` app in the ``pyconsg`` context.

"""
import datetime

from django import forms
from django.utils.translation import ugettext_lazy as _

from symposion.schedule.models import Presentation

from paypal_express_checkout.models import Item
from paypal_express_checkout.forms import SetExpressCheckoutFormMixin

from .models import CheckoutChoices, FOOD_CHOICES, TSHIRT_CHOICES


class CheckoutChoicesForm(forms.ModelForm):
    class Meta:
        model = CheckoutChoices
        fields = (
            'tutorial_morning', 'tutorial_afternoon', 'tshirt_size',
            'food_choice')

    tutorial_morning = forms.ModelChoiceField(
        label=_('Tutorial (morning)'),
        queryset=Presentation.objects.filter(
            proposal_base__kind__slug='tutorial',
            slot__start__lte=datetime.time(13, 0)),
        empty_label=None,
        required=False,
    )

    tutorial_afternoon = forms.ModelChoiceField(
        label=_('Tutorial (afternoon)'),
        queryset=Presentation.objects.filter(
            proposal_base__kind__slug='tutorial',
            slot__start__gt=datetime.time(13, 0)),
        empty_label=None,
        required=False,
    )


    def __init__(self, user, *args, **kwargs):
        kwargs.update({'instance': user.checkout_choices, })
        super(CheckoutChoicesForm, self).__init__(*args, **kwargs)
        if not user.checkout_choices.tutorial_morning:
            self.fields.pop('tutorial_morning')

        if not user.checkout_choices.tutorial_afternoon:
            self.fields.pop('tutorial_afternoon')


class PyconsgGroupSetExpressCheckoutForm(SetExpressCheckoutFormMixin):
    amount_conference_tickets = forms.IntegerField(
        label=_('Conference tickets'),
        required=False,
    )

    amount_student_tickets = forms.IntegerField(
        label=_('Conference tickets (student rate)'),
        required=False,
    )

    amount_tutorials = forms.IntegerField(
        label=_('Tutorial tickets'),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(PyconsgGroupSetExpressCheckoutForm, self).__init__(
            *args, **kwargs)
        self.conference_item = Item.objects.get(identifier='conference')
        self.student_item = Item.objects.get(
            identifier='conference-student')
        self.tutorial_item = Item.objects.get(identifier='tutorial')

    def clean(self):
        data = self.cleaned_data
        if (not data.get('amount_conference_tickets')
                and not data.get('amount_student_tickets')
                and not data.get('amount_tutorials')):
            raise forms.ValidationError(
                'You have to enter at least one conference ticket or one'
                ' tutorial.')
        return data

    def get_items_and_quantities(self):
        """
        Returns the items and quantities.

        Should return a list of tuples.

        """
        data = self.cleaned_data
        result = []
        amount_conference_tickets = data.get('amount_conference_tickets')
        if amount_conference_tickets:
            result.append((self.conference_item, amount_conference_tickets))

        amount_student_tickets = data.get('amount_student_tickets')
        if amount_student_tickets:
            result.append((self.student_item, amount_student_tickets))

        amount_tutorials = data.get('amount_tutorials')
        if amount_tutorials:
            result.append((self.tutorial_item, amount_tutorials))
        return result


class PyconsgSetExpressCheckoutForm(SetExpressCheckoutFormMixin):
    student_rate = forms.BooleanField(
        label=_('I am a student'),
        initial=False,
        widget=forms.CheckboxInput(
            attrs={'style': 'width: 2em; float: left; margin-right: 1em;', }),
        required=False,
    )

    conference_ticket = forms.BooleanField(
        label=_('Conference ticket'),
        initial=True,
        widget=forms.CheckboxInput(
            attrs={'style': 'width: 2em; float: left; margin-right: 1em;', }),
        required=False,
    )

    tutorial_morning = forms.ModelChoiceField(
        label=_('Tutorial (morning)'),
        queryset=Presentation.objects.filter(
            proposal_base__kind__slug='tutorial',
            slot__start__lte=datetime.time(13, 0)),
        required=False,
    )

    tutorial_afternoon = forms.ModelChoiceField(
        label=_('Tutorial (afternoon)'),
        queryset=Presentation.objects.filter(
            proposal_base__kind__slug='tutorial',
            slot__start__gt=datetime.time(13, 0)),
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

    def __init__(self, *args, **kwargs):
        super(PyconsgSetExpressCheckoutForm, self).__init__(*args, **kwargs)
        self.conference_item = Item.objects.get(identifier='conference')
        self.student_item = Item.objects.get(
            identifier='conference-student')
        self.tutorial_item = Item.objects.get(identifier='tutorial')

    def clean(self):
        data = self.cleaned_data
        if (not data.get('conference_ticket')
                and not data.get('tutorial_morning')
                and not data.get('tutorial_afternoon')):
            raise forms.ValidationError(
                'You have to select at least one conference ticket or one'
                ' tutorial.')
        return data

    def get_items_and_quantities(self):
        """
        Returns the items and quantities.

        Should return a list of tuples.

        """
        data = self.cleaned_data
        result = []
        if data['conference_ticket'] and not data['student_rate']:
            result.append((self.conference_item, 1))
        if data['conference_ticket'] and data['student_rate']:
            result.append((self.student_item, 1))
        tutorial_amount = 0
        if data['tutorial_morning']:
            tutorial_amount += 1
        if data['tutorial_afternoon']:
            tutorial_amount += 1
        if tutorial_amount:
            result.append((self.tutorial_item, tutorial_amount))
        return result

    def post_transaction_save(self, transaction, item_quantity_list):
        CheckoutChoices.objects.filter(user=self.user).delete()
        choices = CheckoutChoices.objects.create(
            user=self.user, transaction=transaction)
        choices.is_student = self.cleaned_data.get('student_rate')
        choices.has_conference_ticket = self.cleaned_data.get(
            'conference_ticket')
        choices.tutorial_morning = self.cleaned_data.get('tutorial_morning')
        choices.tutorial_afternoon = self.cleaned_data.get(
            'tutorial_afternoon')
        choices.tshirt_size = self.cleaned_data.get('tshirt_size')
        choices.food_Choice = self.cleaned_data.get('food_choice')
        choices.save()
