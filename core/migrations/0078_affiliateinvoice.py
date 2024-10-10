# Generated by Django 5.1.1 on 2024-10-09 17:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0077_clientprofile_affiliate'),
    ]

    operations = [
        migrations.CreateModel(
            name='AffiliateInvoice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('revenue', models.FloatField(blank=True, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('affiliate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoice_affiliate_profile', to='core.affiliateprofile')),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='client_affiliate_profile', to='core.clientprofile')),
            ],
        ),
    ]
