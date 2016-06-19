"""Imports wifi passwords from a given .csv file."""
import csv

from django.core.management.base import BaseCommand

from optparse import make_option

from paypal_express_checkout.constants import PAYMENT_STATUS
from paypal_pyconsg.models import CheckoutChoices


class Command(BaseCommand):
    help = 'Imports wifi passwords from a given .csv file.'
    option_list = BaseCommand.option_list + (
        make_option('-f', '--file', dest='filename'),
    )

    def handle(self, *args, **options):
        filename = options.get('filename')
        choices = CheckoutChoices.objects.filter(
            transaction__status=PAYMENT_STATUS['completed'])
        choices = choices.order_by('pk')
        choices = choices.iterator()
        with open(filename, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                if row[0] == 'user_id':
                    continue
                try:
                    choice = choices.next()
                except StopIteration:
                    break
                choice.wifi_username = row[0]
                choice.wifi_password = row[1]
                choice.wifi_ssid = row[2]
                choice.save()

        # Print result
        choices = CheckoutChoices.objects.filter(
            transaction__status=PAYMENT_STATUS['completed']).order_by('pk')
        for choice in choices:
            print('{} / {} / {}').format(
                choice.wifi_username,
                choice.wifi_password,
                choice.wifi_ssid,
            )
