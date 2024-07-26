# Generated by Django 5.0.6 on 2024-07-24 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_profile_agents_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='client_status',
            field=models.CharField(blank=True, choices=[('active', 'Active'), ('hold', 'Hold'), ('pending', 'Pending'), ('inactive', 'Inactive')], default='active', max_length=50, null=True),
        ),
    ]
