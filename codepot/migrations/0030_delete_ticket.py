# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0029_auto_20150818_2110'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Ticket',
        ),
    ]
