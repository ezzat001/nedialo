# Generated by Django 5.1.1 on 2024-12-03 18:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0118_role_admin_contracts_role_admin_packages'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='price',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='package',
            name='services',
            field=models.ManyToManyField(blank=True, related_name='package_services', to='core.service'),
        ),
    ]