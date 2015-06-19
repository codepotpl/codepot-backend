# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import codepot.models.promo_codes
from django.conf import settings
import datetime
import codepot
import django.core.validators
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
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('date_from', models.DateTimeField(unique=True)),
                ('date_to', models.DateTimeField(unique=True)),
                ('tickets_purchased', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.CharField(serialize=False, default=codepot.create_hash, primary_key=True, max_length=32)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('price_net', models.IntegerField()),
                ('price_vat', models.FloatField(default=0.23)),
                ('price_tier', models.ForeignKey(to='codepot.PriceTier')),
            ],
        ),
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('code', models.CharField(serialize=False, default=codepot.models.promo_codes._promo_code_value, primary_key=True, max_length=6)),
                ('usage_limit', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0)])),
                ('active', models.BooleanField(default=True)),
                ('discount', models.IntegerField(default=10, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)])),
                ('sent', models.BooleanField(default=False)),
                ('contact_info', models.TextField(default=None, blank=True, null=True)),
                ('notes', models.TextField(default=None, blank=True, null=True)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('valid_from', models.DateField(default=None, blank=True, null=True)),
                ('valid_to', models.DateField(default=None, blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='PromoCodeClassification',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.CharField(serialize=False, default=codepot.models.purchases._purchase_id_value, primary_key=True, max_length=32)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('payment_type', models.CharField(choices=[('PAYU', 'PAYU'), ('TRANSFER', 'TRANSFER'), ('FREE', 'FREE')], max_length=64)),
                ('payment_status', models.CharField(default='PENDING', choices=[('PENDING', 'PENDING'), ('SUCCESS', 'SUCCESS'), ('FAILED', 'FAILED')], max_length=32)),
                ('price_net', models.IntegerField(default=0)),
                ('price_total', models.IntegerField(default=0)),
                ('payu_payment_link', models.URLField(default=None, blank=True, max_length=4096, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('fake', models.BooleanField(default=False)),
                ('confirmation_sent', models.BooleanField(default=False)),
                ('payu_payment', models.OneToOneField(default=None, null=True, to='django_payu.PayuPayment', blank=True)),
                ('product', models.ForeignKey(to='codepot.Product')),
                ('promo_code', models.ForeignKey(to='codepot.PromoCode', null=True, default=None, blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PurchaseInvoice',
            fields=[
                ('id', models.CharField(serialize=False, default=codepot.models.purchases._purchase_id_value, primary_key=True, max_length=32)),
                ('no', models.CharField(blank=True, max_length=256, null=True)),
                ('name', models.CharField(max_length=256)),
                ('street', models.CharField(max_length=256)),
                ('city', models.CharField(max_length=256)),
                ('zip_code', models.CharField(max_length=256)),
                ('country', models.CharField(max_length=256)),
                ('tax_id', models.CharField(max_length=256)),
                ('ifirma_id', models.CharField(blank=True, max_length=256, null=True)),
                ('sent', models.BooleanField(default=False)),
                ('purchase', models.OneToOneField(to='codepot.Purchase', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.CharField(serialize=False, default=codepot.create_hash, primary_key=True, max_length=32)),
                ('created', models.DateTimeField(default=datetime.datetime.now)),
                ('type', models.CharField(choices=[('FIRST_DAY', 'FIRST_DAY'), ('SECOND_DAY', 'SECOND_DAY'), ('BOTH_DAYS', 'BOTH_DAYS')], max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='promocode',
            name='classification',
            field=models.ForeignKey(to='codepot.PromoCodeClassification', null=True, blank=True),
        ),
    ]
