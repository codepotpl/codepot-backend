# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0008_auto_20150531_0935'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchase',
            old_name='invoice_zip',
            new_name='invoice_zip_code',
        ),
    ]
