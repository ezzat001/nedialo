# Generated by Django 5.1.1 on 2024-12-03 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0117_rename_contractservice_package_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='admin_contracts',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='role',
            name='admin_packages',
            field=models.BooleanField(default=False),
        ),
    ]