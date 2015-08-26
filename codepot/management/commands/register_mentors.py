import json
import sys
from optparse import make_option

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction
from getenv import env
from rest_framework.test import APIRequestFactory

from codepot import create_hash
from codepot.models import (
  PromoCode,
  Purchase,
  Product,
  WorkshopMentor,
  PaymentStatusName,
  PaymentTypeName,
)
from codepot.utils import get_rendered_template
from codepot.views.auth import sign_up
from celerytq.tasks import send_mail
from main import settings


class Command(BaseCommand):
  option_list = (
    make_option('-f', '--file',
                dest='mentors_json',
                help='Path to file with mentors JSON data'),
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

  def _add_purchase(self, user):

    promo_code = PromoCode.objects.get(code=env('CDPT_MENTORS_PROMO_CODE'))
    product = Product.objects.order_by('id')[0]

    Purchase.objects.create(
      user=user, promo_code=promo_code, product=product,
      payment_status=PaymentStatusName.SUCCESS.value,
      payment_type=PaymentTypeName.FREE.value
    )

  def _send_reset_password_message(self, user):
    reset_link = '{}{}'.format(settings.WEB_CLIENT_ADDRESS, 'reset-password')
    ctx = {
      'name': '{} {}'.format(user.first_name, user.last_name),
      'reset_link': reset_link
    }
    send_mail.delay(
      [user.email], 'Codepot Reset Password Request ({})'.format(user.email),
      get_rendered_template('mail/mentor_registration_confirmation.txt', ctx),
      get_rendered_template('mail/mentor_registration_confirmation.html', ctx),
      ['tickets@codepot.pl']
    )

  def _create_workshop_mentor_model(self, user, entry):
    workshop_mentor = WorkshopMentor.objects.get_or_create(user=user)[0]

    workshop_mentor.first_name = entry['firstName']
    workshop_mentor.last_name = entry['lastName']
    workshop_mentor.tagline = entry['tagline']
    workshop_mentor.picture_url = entry['pictureUrl']
    workshop_mentor.twitter_username = entry['twitterUsername']
    workshop_mentor.github_username = entry['githubUsername']
    workshop_mentor.linkedin_profile_url = entry['linkedInProfileUrl']
    workshop_mentor.stackoverflow_id = entry['stackoverflowId']
    workshop_mentor.googleplus_handler = entry['googlePlusHandler']
    workshop_mentor.website_url = entry['websiteUrl']
    workshop_mentor.bio_in_md = entry['bioInMd']

    workshop_mentor.save()

  def handle(self, *args, **options):
    mentors_json = options.get('mentors_json')

    if mentors_json is None:
      self.stderr.write('No mentors JSON file passed.')
      sys.exit(1)

    self.stdout.write("Loading data from: '{}' file".format(mentors_json))

    with open(mentors_json) as file:
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
              self._add_purchase(user)
              self._send_reset_password_message(user)

            else:
              self.stderr.write(
                'User with email: {} (ID: {}) already exists, skipping registration.'.format(email, user.id))
              user = self._find_user_for_email_or_none(email)
              self._create_workshop_mentor_model(user, entry)


        except Exception as e:
          self.stderr.write('Error while processing user with email: {}, err: {}'.format(email, e))
