# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import datetime
import django.core.validators
import codepot
import codepot.models.promo_codes
import codepot.models.purchases


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('django_payu', '0003_payupayment_continue_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='PriceTier',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('date_from', models.DateTimeField(unique=True)),
                ('date_to', models.DateTimeField(unique=True)),
                ('tickets_purchased', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.CharField(default=codepot.create_hash, max_length=32, primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('price_net', models.IntegerField()),
                ('price_vat', models.FloatField(default=0.23)),
                ('price_tier', models.ForeignKey(to='codepot.PriceTier')),
            ],
        ),
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('code', models.CharField(default=codepot.models.promo_codes._promo_code_value, max_length=6, primary_key=True, serialize=False)),
                ('usage_limit', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], default=1)),
                ('active', models.BooleanField(default=True)),
                ('discount', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], default=10)),
                ('sent', models.BooleanField(default=False)),
                ('contact_info', models.TextField(null=True, blank=True, default=None)),
                ('notes', models.TextField(null=True, blank=True, default=None)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('valid_from', models.DateField(null=True, blank=True, default=None)),
                ('valid_to', models.DateField(null=True, blank=True, default=None)),
            ],
        ),
        migrations.CreateModel(
            name='PromoCodeClassification',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(unique=True, max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.CharField(default=codepot.models.purchases._purchase_id_value, max_length=32, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('payment_type', models.CharField(max_length=64, choices=[('PAYU', 'PAYU'), ('TRANSFER', 'TRANSFER'), ('FREE', 'FREE')])),
                ('payment_status', models.CharField(default='PENDING', max_length=32, choices=[('PENDING', 'PENDING'), ('SUCCESS', 'SUCCESS'), ('FAILED', 'FAILED')])),
                ('price_net', models.IntegerField(default=0)),
                ('price_total', models.IntegerField(default=0)),
                ('payu_payment_link', models.URLField(null=True, max_length=4096, blank=True, default=None)),
                ('notes', models.TextField(null=True, blank=True)),
                ('payu_payment', models.OneToOneField(blank=True, default=None, to='django_payu.PayuPayment', null=True)),
                ('product', models.ForeignKey(to='codepot.Product')),
                ('promo_code', models.ForeignKey(to='codepot.PromoCode', blank=True, default=None, null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseInvoice',
            fields=[
                ('id', models.CharField(default=codepot.models.purchases._purchase_id_value, max_length=32, primary_key=True, serialize=False)),
                ('no', models.CharField(null=True, max_length=256, blank=True)),
                ('name', models.CharField(max_length=256)),
                ('street', models.CharField(max_length=256)),
                ('city', models.CharField(max_length=256)),
                ('zip_code', models.CharField(max_length=256)),
                ('country', models.CharField(max_length=256)),
                ('tax_id', models.CharField(max_length=256)),
                ('ifirma_id', models.CharField(null=True, max_length=256, blank=True)),
                ('sent', models.BooleanField(default=False)),
                ('purchase', models.OneToOneField(blank=True, to='codepot.Purchase', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.CharField(default=codepot.create_hash, max_length=32, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('type', models.CharField(max_length=64, choices=[('FIRST_DAY', 'FIRST_DAY'), ('SECOND_DAY', 'SECOND_DAY'), ('BOTH_DAYS', 'BOTH_DAYS')])),
            ],
        ),
        migrations.AddField(
            model_name='promocode',
            name='classification',
            field=models.ForeignKey(to='codepot.PromoCodeClassification', blank=True, null=True),
        ),
    ]
