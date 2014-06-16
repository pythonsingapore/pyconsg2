"""Models for the PayPal integration of the ``pyconsg`` project."""
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.translation import ugettext_lazy as _


FOOD_CHOICES = (
    ('', 'No preference'),
    ('V', 'Vegetarian'),
    ('VG', 'Vegan'),
)


TSHIRT_CHOICES = (
    ('XS', 'XS'),
    ('S', 'S'),
    ('M', 'M'),
    ('L', 'L'),
    ('XL', 'XL'),
    ('XXL', 'XXL'),
    ('XXXL', 'XXXL'),
)


class CheckoutChoices(models.Model):
    """
    Model to save the choices the user made during checkout.

    :user: The user who made the choices
    :transaction: The PaymentTransaction. We need this in order to know if the
      payment actually went through and the user is actualyl entitled to see
      the chosen tutorials.
    :tutorial_morning: The tutorial the user selected for the morning session
      (optional).
    :tutorial_afternoon: The tutorial the user selected for the afternoon
      session (optional).
    :tshirt_size: The t-shirt size the user selected.

    """
    user = models.OneToOneField(
        'auth.User',
        verbose_name=_('User'),
        related_name='checkout_choices',
    )

    transaction = models.ForeignKey(
        'paypal_express_checkout.PaymentTransaction',
        verbose_name=_('Transaction'),
        related_name='checkout_choices',
    )

    is_student = models.BooleanField(
        default=False,
        verbose_name=_('Is student'),
    )

    has_conference_ticket = models.BooleanField(
        default=False,
        verbose_name=_('Has conference ticket'),
    )

    tutorial_morning = models.ForeignKey(
        'schedule.Presentation',
        verbose_name=('Tutorial (morning)'),
        related_name='choices_tutorial_morning',
        null=True, blank=True,
    )

    tutorial_afternoon = models.ForeignKey(
        'schedule.Presentation',
        verbose_name=('Tutorial (afternoon)'),
        related_name='choices_tutorial_afternoon',
        null=True, blank=True,
    )

    tshirt_size = models.CharField(
        max_length=5,
        choices=TSHIRT_CHOICES,
        verbose_name=_('T-Shirt size'),
        null=True, blank=True,
    )

    food_choice = models.CharField(
        max_length=5,
        choices=FOOD_CHOICES,
        verbose_name=_('Food preference'),
        null=True, blank=True,
    )

    is_registered = models.BooleanField(
        default=False,
        verbose_name=_('Is registered'),
        blank=True,
    )

    def get_food_choice(self):
        for choice in FOOD_CHOICES:
            if choice[0] == self.food_choice:
                return choice[1]
        return ''

    def is_speaker_yesno(self):
        try:
            self.user.speaker_profile
        except ObjectDoesNotExist:
            return 'No'
        if self.user.speaker_profile.presentations.all():
            return 'Yes'
        return 'No'

    def is_student_yesno(self):
        return self.is_student and 'Yes' or 'No'

    def has_conference_ticket_yesno(self):
        return self.has_conference_ticket and 'Yes' or 'No'

    def tutorial_morning_yesno(self):
        if self.tutorial_morning:
            return 'Yes'
        return 'No'

    def tutorial_afternoon_yesno(self):
        if self.tutorial_afternoon:
            return 'Yes'
        return 'No'
