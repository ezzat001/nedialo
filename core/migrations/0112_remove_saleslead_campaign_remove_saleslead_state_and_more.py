# Generated by Django 5.1.1 on 2024-11-20 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0111_lead_appointment_time_lead_contractor_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='saleslead',
            name='campaign',
        ),
        migrations.RemoveField(
            model_name='saleslead',
            name='state',
        ),
        migrations.AddField(
            model_name='serversetting',
            name='sales_webhook',
            field=models.TextField(blank=True, null=True),
        ),
    ]
