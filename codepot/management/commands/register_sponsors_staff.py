import json
import sys
from optparse import make_option

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction

from rest_framework.test import APIRequestFactory

from codepot import create_hash
from codepot.models import (
  PromoCode,
  Purchase,
  Product,
  PaymentStatusName,
  PaymentTypeName,
)
from codepot.views.auth import sign_up


class Command(BaseCommand):
  option_list = (
    make_option('-f', '--file',
                dest='sponsors_json',
                help='Path to file with sponsors JSON data'),
  )
  factory = APIRequestFactory()

  def _find_user_for_email_or_none(self, email):
    try:
      return User.objects.get(email=email)
    except User.DoesNotExist:
      return None

  def _sign_up(self, entry):
    request = self.factory.post('', {
      'firstName': entry['firstName'],
      'lastName': entry['lastName'],
      'email': entry['email'],
      'password': create_hash(length=10),
    }, format='json')

    sign_up(request)

  def _add_purchase(self, user, promo_code):

    promo_code = PromoCode.objects.get(code=promo_code)
    product = Product.objects.order_by('id')[0]

    Purchase.objects.create(
      user=user, promo_code=promo_code, product=product,
      payment_status=PaymentStatusName.SUCCESS.value,
      payment_type=PaymentTypeName.FREE.value
    )

  def handle(self, *args, **options):
    sponsors_json = options.get('sponsors_json')

    if sponsors_json is None:
      self.stderr.write('No sponsors JSON file passed.')
      sys.exit(1)

    self.stdout.write("Loading data from: '{}' file".format(sponsors_json))

    with open(sponsors_json) as file:
      data = json.load(file)

      for entry in data:
        email = entry['email']

        self.stdout.write(
          'Processing user with email: {}, first name: {}, last name: {}'.
            format(email, entry['firstName'], entry['lastName'])
        )

        try:

          with transaction.atomic():

            user = self._find_user_for_email_or_none(email)

            if user is None:

              self._sign_up(entry)
              user = self._find_user_for_email_or_none(email)
              self._add_purchase(user, entry['promoCode'])

            else:
              self.stderr.write(
                'User with email: {} (ID: {}) already exists, skipping registration.'.format(email, user.id))

        except Exception as e:
          self.stderr.write('Error while processing user with email: {}, err: {}'.format(email, e))
