# Generated by Django 5.0.6 on 2024-08-19 17:23

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0043_workstatus_offline_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workstatus',
            name='date',
        ),
        migrations.RemoveField(
            model_name='workstatus',
            name='user',
        ),
        migrations.AlterField(
            model_name='workstatus',
            name='current_status',
            field=models.CharField(choices=[('ready', 'Ready'), ('meeting', 'Meeting'), ('break', 'Break'), ('offline', 'Offline')], max_length=10),
        ),
        migrations.AlterField(
            model_name='workstatus',
            name='last_status_change',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]