# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import codepot.models.purchases


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0010_auto_20150602_1919'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseInvoice',
            fields=[
                ('id', models.CharField(serialize=False, primary_key=True, max_length=32, default=codepot.models.purchases._purchase_id_value)),
                ('name', models.CharField(null=True, max_length=256, blank=True)),
                ('street', models.CharField(null=True, max_length=256, blank=True)),
                ('zip_code', models.CharField(null=True, max_length=256, blank=True)),
                ('country', models.CharField(null=True, max_length=256, blank=True)),
                ('tax_id', models.CharField(null=True, max_length=256, blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='invoice_country',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='invoice_name',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='invoice_street',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='invoice_tax_id',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='invoice_zip_code',
        ),
        migrations.AddField(
            model_name='purchase',
            name='invoice',
            field=models.OneToOneField(null=True, blank=True, to='codepot.PurchaseInvoice'),
        ),
    ]
