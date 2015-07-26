# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0012_workshopmessage_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='workshopmessage',
            name='created',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
