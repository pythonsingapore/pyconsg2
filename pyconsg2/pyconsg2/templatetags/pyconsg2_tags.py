"""Templatetags for the pyconsg2 project."""
from django import template
from django.db.models import Q

from cms.models.static_placeholder import StaticPlaceholder
from paypal_express_checkout.models import PurchasedItem
from paypal_express_checkout.constants import PAYMENT_STATUS
from symposion.schedule.models import Presentation

from paypal_pyconsg.models import CheckoutChoices


register = template.Library()


@register.assignment_tag
def inspect(obj):
    import ipdb
    ipdb.set_trace()
    return obj


@register.assignment_tag
def get_static_placeholders():
    return StaticPlaceholder.objects.all()


@register.assignment_tag
def get_early_bird_count(ticket_amount):
    count = ticket_amount - PurchasedItem.objects.filter(
        transaction__status='Completed',
        item__identifier__in=['conference-early', 'conference-student-early', ],
    ).count()
    if count < 0:
        count = 0
    return count


@register.assignment_tag
def get_checkout_choices(user):
    """Returns completed checkout choices for the given user."""
    choices = user.checkout_choices.filter(
        has_conference_ticket=True,
        transaction__status=PAYMENT_STATUS['completed'])
    if choices:
        return choices[0]
    return None


@register.assignment_tag
def get_tutorials(user):
    """Returns all accepted tutorials for the given user."""
    return Presentation.objects.filter(
        speaker__user=user, proposal_base__kind__slug='tutorial')


@register.assignment_tag
def get_tutorial_attendees(tutorial):
    """Returns completed CheckoutChoices that have the given tutorial."""
    return CheckoutChoices.objects.filter(
        transaction__status='Completed').filter(
        Q(tutorial_morning=tutorial) | Q(tutorial_afternoon=tutorial))
