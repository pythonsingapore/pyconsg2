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


# Change those to the non-early versions when early bird phase ends
CURRENT_CONFERENCE_ITEM = 'conference-early'
CURRENT_CONFERENCE_STUDENT_ITEM = 'conference-student-early'
# CURRENT_TUTORIAL_ITEM = 'tutorial-early'
# CURRENT_CONFERENCE_ITEM = 'conference'
# CURRENT_CONFERENCE_STUDENT_ITEM = 'conference-student'
CURRENT_TUTORIAL_ITEM = 'tutorial'


class CheckoutChoicesForm(forms.Form):
    class Meta:
        fields = (
            'tutorial_morning', 'tutorial_afternoon', 'tshirt_size',
            'food_choice')

    tutorial_morning = forms.ModelChoiceField(
        label=_('Tutorial (morning)'),
        queryset=Presentation.objects.filter(
            available_for_purchase=True,
            proposal_base__kind__slug='tutorial',
            slot__start__lte=datetime.time(13, 0)),
        empty_label=None,
        required=False,
    )

    tutorial_afternoon = forms.ModelChoiceField(
        label=_('Tutorial (afternoon)'),
        queryset=Presentation.objects.filter(
            available_for_purchase=True,
            proposal_base__kind__slug='tutorial',
            slot__start__gt=datetime.time(13, 0)),
        empty_label=None,
        required=False,
    )

    tshirt_size = forms.ChoiceField(
        choices=TSHIRT_CHOICES, required=True,
    )

    food_choice = forms.ChoiceField(
        choices=FOOD_CHOICES, required=False,
    )

    def __init__(self, user, *args, **kwargs):
        super(CheckoutChoicesForm, self).__init__(*args, **kwargs)
        self.choices = CheckoutChoices.objects.get_for_user(user)

        tutorial_morning = CheckoutChoices.objects.get_tutorial_morning(
            user, self.choices)
        if not tutorial_morning:
            self.fields.pop('tutorial_morning')
        else:
            self.initial['tutorial_morning'] = tutorial_morning

        tutorial_afternoon = CheckoutChoices.objects.get_tutorial_afternoon(
            user, self.choices)
        if not tutorial_afternoon:
            self.fields.pop('tutorial_afternoon')
        else:
            self.initial['tutorial_afternoon'] = tutorial_afternoon

        tshirt_size = CheckoutChoices.objects.get_tshirt_size(
            user, self.choices)
        self.initial['tshirt_size'] = tshirt_size

        food_choice = CheckoutChoices.objects.get_tshirt_size(
            user, self.choices)
        self.initial['food_choice'] = food_choice

    def save(self, *args, **kwargs):
        """
        Saves the choices into the user's latest ``CheckoutChoices`` object.

        """
        choices = self.choices[0]
        choices.tutorial_morning = self.cleaned_data.get('tutorial_morning')
        choices.tutorial_afternoon = self.cleaned_data.get(
            'tutorial_afternoon')
        choices.tshirt_size = self.cleaned_data.get('tshirt_size')
        choices.food_choice = self.cleaned_data.get('food_choice')
        choices.save()
        return choices


class PyconsgGroupSetExpressCheckoutForm(SetExpressCheckoutFormMixin):
    amount_conference_tickets = forms.IntegerField(
        label=_('Conference tickets'),
        min_value=1,
        required=False,
    )

    amount_student_tickets = forms.IntegerField(
        label=_('Conference tickets (student rate)'),
        min_value=1,
        required=False,
    )

    amount_tutorials = forms.IntegerField(
        label=_('Tutorial tickets'),
        min_value=1,
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super(PyconsgGroupSetExpressCheckoutForm, self).__init__(
            *args, **kwargs)
        self.conference_item = Item.objects.get(
            identifier=CURRENT_CONFERENCE_ITEM)
        self.student_item = Item.objects.get(
            identifier=CURRENT_CONFERENCE_STUDENT_ITEM)
        self.tutorial_item = Item.objects.get(
            identifier=CURRENT_TUTORIAL_ITEM)

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
            result.append((
                self.conference_item, amount_conference_tickets, None))

        amount_student_tickets = data.get('amount_student_tickets')
        if amount_student_tickets:
            result.append((self.student_item, amount_student_tickets, None))

        amount_tutorials = data.get('amount_tutorials')
        if amount_tutorials:
            result.append((self.tutorial_item, amount_tutorials, None))
        return result


class PyconsgGroupEarlyBirdSetExpressCheckoutForm(
        PyconsgGroupSetExpressCheckoutForm):
    def __init__(self, *args, **kwargs):
        super(PyconsgGroupSetExpressCheckoutForm, self).__init__(
            *args, **kwargs)
        self.conference_item = Item.objects.get(
            identifier='conference-early')
        self.student_item = Item.objects.get(
            identifier='conference-student-early')
        self.tutorial_item = Item.objects.get(
            identifier='tutorial-early')


class PyconsgSetExpressCheckoutForm(SetExpressCheckoutFormMixin):
    student_rate = forms.BooleanField(
        label=_('I am a student'),
        initial=False,
        required=False,
    )

    conference_ticket = forms.BooleanField(
        label=_('Conference ticket'),
        initial=True,
        required=False,
    )

    tutorial_morning = forms.ModelChoiceField(
        label=_('Tutorial (morning)'),
        queryset=Presentation.objects.filter(
            available_for_purchase=True,
            proposal_base__kind__slug='tutorial',
            slot__start__lte=datetime.time(13, 0)),
        required=False,
    )

    tutorial_afternoon = forms.ModelChoiceField(
        label=_('Tutorial (afternoon)'),
        queryset=Presentation.objects.filter(
            available_for_purchase=True,
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
        self.conference_item = Item.objects.get(
            identifier=CURRENT_CONFERENCE_ITEM)
        self.student_item = Item.objects.get(
            identifier=CURRENT_CONFERENCE_STUDENT_ITEM)
        self.tutorial_item = Item.objects.get(
            identifier=CURRENT_TUTORIAL_ITEM)

    def clean(self):
        data = self.cleaned_data
        choices = CheckoutChoices.objects.get_for_user(self.user)
        if choices:
            if CheckoutChoices.objects.has_conference_ticket(
                    self.user, choices):
                if data.get('conference_ticket'):
                    raise forms.ValidationError(
                        'You have already purchased a conference ticket.'
                        ' If you would like to purchase another ticket on'
                        ' behalf of someone else, please create a new account'
                        ' for that person.')
            if CheckoutChoices.objects.has_tutorial_morning(
                    self.user, choices):
                if data.get('tutorial_morning'):
                    raise forms.ValidationError(
                        'You have already purchased a morning tutorial.'
                        ' If you would like to purchase another one on'
                        ' behalf of someone else, please create a new account'
                        ' for that person.')
            if CheckoutChoices.objects.has_tutorial_afternoon(
                    self.user, choices):
                if data.get('tutorial_afternoon'):
                    raise forms.ValidationError(
                        'You have already purchased an afternoon tutorial.'
                        ' If you would like to purchase another one on'
                        ' behalf of someone else, please create a new account'
                        ' for that person.')
        if (not data.get('conference_ticket')
                and not data.get('tutorial_morning')
                and not data.get('tutorial_afternoon')):
            raise forms.ValidationError(
                'You have to select at least one conference ticket or one'
                ' tutorial.')
        return data

    def get_items_and_quantities(self):
        """
        Returns the items, quantities and content types.

        Should return a list of tuples.

        """
        data = self.cleaned_data
        result = []
        if data['conference_ticket'] and not data['student_rate']:
            result.append((self.conference_item, 1, None))
        if data['conference_ticket'] and data['student_rate']:
            result.append((self.student_item, 1, None))
        tutorial_amount = 0
        if data['tutorial_morning']:
            tutorial_amount += 1
        if data['tutorial_afternoon']:
            tutorial_amount += 1
        if tutorial_amount:
            result.append((self.tutorial_item, tutorial_amount, None))
        return result

    def post_transaction_save(self, transaction, item_quantity_list):
        choices = CheckoutChoices.objects.create(
            user=self.user, transaction=transaction)
        choices.is_student = self.cleaned_data.get('student_rate')
        choices.has_conference_ticket = self.cleaned_data.get(
            'conference_ticket')
        choices.tutorial_morning = self.cleaned_data.get(
            'tutorial_morning')
        choices.tutorial_afternoon = self.cleaned_data.get(
            'tutorial_afternoon')
        choices.tshirt_size = self.cleaned_data.get('tshirt_size')
        choices.food_choice = self.cleaned_data.get('food_choice')
        choices.save()
