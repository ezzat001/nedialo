# Generated by Django 5.1.1 on 2024-12-24 02:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0140_contractpref_above_market_perc_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='serversetting',
            name='clients_webhook',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='contractpref',
            name='property_type_re',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]
