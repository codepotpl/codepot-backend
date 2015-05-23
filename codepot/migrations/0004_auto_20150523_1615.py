# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import codepot.models.promo_codes


class Migration(migrations.Migration):

    dependencies = [
        ('codepot', '0003_purchase'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('promo_code_id', models.CharField(serialize=False, max_length=6, primary_key=True, default=codepot.models.promo_codes._promo_code_value)),
            ],
        ),
        migrations.AddField(
            model_name='purchase',
            name='promo_code',
            field=models.ForeignKey(to='codepot.PromoCode', default=None, blank=True, null=True),
        ),
    ]
