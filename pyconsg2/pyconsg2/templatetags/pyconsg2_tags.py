"""Templatetags for the pyconsg2 project."""
from django import template

from cms.models.static_placeholder import StaticPlaceholder
from paypal_express_checkout.models import PurchasedItem
from paypal_express_checkout.constants import PAYMENT_STATUS


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
