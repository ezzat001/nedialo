# Generated by Django 5.1.1 on 2024-12-05 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0129_contractvisit_contract'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='paid',
            field=models.BooleanField(default=False),
        ),
    ]