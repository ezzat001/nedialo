# Generated by Django 5.1.1 on 2024-09-25 12:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0064_remove_saleslead_lead_flow_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='saleslead',
            name='handled',
        ),
    ]
