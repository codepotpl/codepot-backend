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

    Purchase.objects.create(user=user, promo_code=promo_code, product=product)

  def _send_reset_password_message(self, user):
    reset_link = '{}{}'.format(settings.WEB_CLIENT_ADDRESS, 'reset-password')
    ctx = {
      'name': '{} {}'.format(user.first_name, user.last_name),
      'reset_link': reset_link
    }
    send_mail.delay(
      user.email, 'Codepot Reset Password Request ({})'.format(user.email),
      get_rendered_template('mail/mentor_registration_confirmation.txt', ctx),
      get_rendered_template('mail/mentor_registration_confirmation.html', ctx),
      ['tickets@codepot.pl']
    )

  def _create_workshop_mentor_model(self, user, entry):
    WorkshopMentor.objects.create(
      user=user,
      first_name=entry['firstName'],
      last_name=entry['lastName'],
      tagline=entry['tagline'],
      picture_url=entry['pictureUrl'],
      twitter_username=entry['twitterUsername'],
      github_username=entry['githubUsername'],
      linkedin_profile_url=entry['linkedInProfileUrl'],
      stackoverflow_id=entry['stackoverflowId'],
      googleplus_handler=entry['googlePlusHandler'],
      website_url=entry['websiteUrl'],
      bio_in_md=entry['bioInMd']
    )

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

        with transaction.atomic():
          try:
            self._sign_up(entry)
            user = User.objects.get(email=email)
            self._add_purchase(user)
            self._send_reset_password_message(user)
            self._create_workshop_mentor_model(user, entry)

          except Exception as e:
            self.stderr.write('Error while processing user with email: {}, err: {}'.format(email, e))
