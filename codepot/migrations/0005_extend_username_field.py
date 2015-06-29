# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0004_auto_20150624_1926'),
    ]

    operations = [
        migrations.RunSQL('ALTER TABLE auth_user ALTER COLUMN username TYPE varchar(254);'),
        migrations.RunSQL('ALTER TABLE auth_user ALTER COLUMN first_name TYPE varchar(254);'),
        migrations.RunSQL('ALTER TABLE auth_user ALTER COLUMN last_name TYPE varchar(254);'),
        migrations.RunSQL('ALTER TABLE auth_user ALTER COLUMN email TYPE varchar(254);'),
    ]
