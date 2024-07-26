# Generated by Django 5.0.6 on 2024-07-22 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_alter_profile_national_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='team_type',
            field=models.CharField(blank=True, choices=[('callers', 'Cold Callers'), ('sales', 'Sales'), ('dispo', 'Dispositions'), ('acq', 'Acquisitions'), ('data', 'Data Management'), ('quality', 'Quality'), ('team_leaders', 'team_leaders')], max_length=50, null=True),
        ),
    ]
