# Generated by Django 5.1.1 on 2024-11-14 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0107_alter_campaign_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='workstatus',
            name='lateness',
            field=models.TimeField(blank=True, null=True),
        ),
    ]
