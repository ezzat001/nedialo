# Generated by Django 5.1.1 on 2024-11-06 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0099_remove_serversetting_hide_campaign_leadform_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serversetting',
            name='company_website',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
