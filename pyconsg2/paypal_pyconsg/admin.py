"""Admin classes for the ``paypal_pyconsg`` app."""
import datetime

from django.contrib import admin
from django.contrib.admin.filters import RelatedFieldListFilter

from symposion.schedule.models import Presentation

from .models import CheckoutChoices


class CheckoutChoicesAdmin(admin.ModelAdmin):
    template = 'admin/checkout_choices_change_list.html'
    model = CheckoutChoices
    list_display = [
        'id', 'user__email', 'user__first_name', 'user__last_name',
        'transaction', 'transaction__status', 'is_student_yesno',
        'has_conference_ticket_yesno', 'tutorial_morning',
        'tutorial_afternoon', 'tshirt_size', 'food_choice', ]
    list_filter = [
        'transaction__status', 'has_conference_ticket', 'is_student',
        'food_choice', 'tshirt_size', 'tutorial_morning',
        'tutorial_afternoon']
    search_fields = [
        'id', 'user__email', 'user__first_name', 'user__last_name',
        'transaction__transaction_id', 'tutorial_morning__title',
        'tutorial_afternoon__title']
    raw_id_fields = ['user', 'transaction', ]

    def is_student_yesno(self, obj):
        return obj.is_student and 'yes' or 'no'

    def has_conference_ticket_yesno(self, obj):
        return obj.has_conference_ticket and 'yes' or 'no'


    def user__email(self, obj):
        return obj.user.email

    def user__first_name(self, obj):
        return obj.user.first_name

    def user__last_name(self, obj):
        return obj.user.last_name

    def transaction__status(self, obj):
        return obj.transaction.status


admin.site.register(CheckoutChoices, CheckoutChoicesAdmin)
