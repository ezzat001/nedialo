# Generated by Django 5.1.1 on 2024-09-17 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0058_remove_application_date_remove_application_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
