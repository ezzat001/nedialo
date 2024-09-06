# Generated by Django 5.0.6 on 2024-09-03 15:29

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0051_absence_team_alter_absence_absence_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeatAssignmentLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('end_time', models.DateTimeField(blank=True, null=True)),
                ('agent_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.profile')),
                ('dialer_credentials', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.dialercredentials')),
            ],
        ),
    ]
