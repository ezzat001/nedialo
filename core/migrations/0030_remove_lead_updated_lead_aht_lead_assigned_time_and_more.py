# Generated by Django 5.0.6 on 2024-08-18 01:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0029_team_team_leader'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lead',
            name='updated',
        ),
        migrations.AddField(
            model_name='lead',
            name='aht',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lead',
            name='assigned_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lead',
            name='handled',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
