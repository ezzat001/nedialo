# Generated by Django 5.0.6 on 2024-07-24 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0035_alter_profile_services'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='joining_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
