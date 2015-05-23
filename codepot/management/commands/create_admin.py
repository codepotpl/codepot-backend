import os

from django.core.management.base import (
    BaseCommand,
    CommandError
)
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    admin_username = 'admin@codepot.pl'
    admin_email = admin_username
    admin_password_env_name = 'CDPT_ADMIN_PASS'

    help = 'Create admin with password from {} env variable.'.format(admin_password_env_name)

    def handle(self, *args, **options):
        try:
            User.objects.get(username=self.admin_username)
            raise CommandError('Admin already exists.')
        except User.DoesNotExist:
            if self.admin_password_env_name not in os.environ:
                raise CommandError(
                    'You need to set admin password in {} env variable.'.format(self.admin_password_env_name)
                )
            admin_password = os.environ[self.admin_password_env_name]
            self.stdout.write('Creating admin with username: {} and password from env variable: {}'.format(
                self.admin_username,
                self.admin_password_env_name,
            ))
            self._create_admin(admin_password)

    def _create_admin(self, password):
        assert password
        User.objects.create_superuser(
            username=self.admin_username,
            email=self.admin_email,
            password=password,
        )
