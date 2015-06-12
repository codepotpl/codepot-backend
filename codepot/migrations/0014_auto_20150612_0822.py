# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0013_auto_20150612_0805'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseinvoice',
            name='no',
            field=models.CharField(default=None, max_length=256),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='purchaseinvoice',
            name='country',
            field=models.CharField(default=None, max_length=256),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='purchaseinvoice',
            name='name',
            field=models.CharField(default=None, max_length=256),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='purchaseinvoice',
            name='street',
            field=models.CharField(default=None, max_length=256),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='purchaseinvoice',
            name='tax_id',
            field=models.CharField(default=None, max_length=256),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='purchaseinvoice',
            name='zip_code',
            field=models.CharField(default=None, max_length=256),
            preserve_default=False,
        ),
    ]
