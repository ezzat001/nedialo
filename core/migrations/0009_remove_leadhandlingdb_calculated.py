# Generated by Django 5.0.6 on 2024-08-07 21:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_leadhandlingdb_calculated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='leadhandlingdb',
            name='calculated',
        ),
    ]
