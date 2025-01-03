# Generated by Django 5.1.1 on 2024-12-03 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0120_remove_package_price_remove_package_services_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractSample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
    ]
