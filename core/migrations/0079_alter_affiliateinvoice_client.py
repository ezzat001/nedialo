# Generated by Django 5.1.1 on 2024-10-09 17:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0078_affiliateinvoice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='affiliateinvoice',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='invoice_client_profile', to='core.clientprofile'),
        ),
    ]
