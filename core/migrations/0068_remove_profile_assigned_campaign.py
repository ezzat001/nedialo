# Generated by Django 5.1.1 on 2024-09-27 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0067_serversetting_sales_lookerstudio_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='assigned_campaign',
        ),
    ]
