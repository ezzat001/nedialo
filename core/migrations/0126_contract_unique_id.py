# Generated by Django 5.1.1 on 2024-12-05 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0125_contract'),
    ]

    operations = [
        migrations.AddField(
            model_name='contract',
            name='unique_id',
            field=models.CharField(blank=True, editable=False, max_length=10, unique=True),
        ),
    ]
