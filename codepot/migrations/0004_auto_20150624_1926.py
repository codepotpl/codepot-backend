# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from codepot.models import AppSettingName


class Migration(migrations.Migration):
    def initial_data(apps, schema_editor):
        AppSettings = apps.get_model('codepot', 'AppSettings')
        AppSettings.objects.create(name=AppSettingName.CDPT_REGISTRATION_OPEN.value, value=True)

    def remove_data(apps, schema_editor):
        AppSettings = apps.get_model('codepot', 'AppSettings')
        AppSettings.objects.all().delete()

    dependencies = [
        ('codepot', '0003_appsettings'),
    ]

    operations = [
        migrations.RunPython(initial_data, reverse_code=remove_data)
    ]
