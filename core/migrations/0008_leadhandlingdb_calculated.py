# Generated by Django 5.0.6 on 2024-08-07 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_lead_property_type_alter_lead_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='leadhandlingdb',
            name='calculated',
            field=models.BooleanField(default=False),
        ),
    ]
