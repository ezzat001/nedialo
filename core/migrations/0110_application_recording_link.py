# Generated by Django 5.1.1 on 2024-11-14 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0109_workstatus_lateness_status_alter_workstatus_lateness'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='recording_link',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]