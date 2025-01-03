# Generated by Django 5.1.1 on 2024-10-09 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0075_alter_affiliateprofile_discovery_method_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='affiliateprofile',
            name='commission_percentage',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='affiliateprofile',
            name='settings_theme',
            field=models.CharField(choices=[('white', 'White'), ('dark', 'Dark')], default='dark', max_length=50),
        ),
        migrations.AlterField(
            model_name='clientprofile',
            name='settings_theme',
            field=models.CharField(choices=[('white', 'White'), ('dark', 'Dark')], default='dark', max_length=50),
        ),
    ]
