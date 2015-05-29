# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='purchase',
        ),
        migrations.AddField(
            model_name='purchase',
            name='invoice_country',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='purchase',
            name='invoice_name',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='purchase',
            name='invoice_street',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='purchase',
            name='invoice_tax_id',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='purchase',
            name='invoice_zip',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='purchase',
            name='ticket',
            field=models.OneToOneField(default=None, to='codepot.Ticket'),
            preserve_default=False,
        ),
    ]
