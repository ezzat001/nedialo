# Generated by Django 5.1.1 on 2024-12-05 03:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0127_contractvisit'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contractvisit',
            old_name='country',
            new_name='location',
        ),
    ]
