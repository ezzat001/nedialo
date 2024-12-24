# Generated by Django 5.1.1 on 2024-12-23 20:06

import core.models
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0136_contract_field'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractPref',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.CharField(blank=True, max_length=100, null=True)),
                ('company_name', models.CharField(blank=True, max_length=100, null=True)),
                ('mention_company', models.BooleanField(default=False)),
                ('propety_type', models.CharField(blank=True, choices=[('residential', 'Residential'), ('commercial', 'Commercial'), ('both', 'Residential & Commercial')], max_length=100, null=True)),
                ('owner_type', models.CharField(blank=True, choices=[('individual', 'Individual'), ('corporate', 'Corporate'), ('any', 'Any')], max_length=100, null=True)),
                ('price_range', models.JSONField(blank=True, default=list, null=True)),
                ('coverage', models.TextField(blank=True, null=True)),
                ('standout', models.TextField(blank=True, null=True)),
                ('questions', models.TextField(blank=True, null=True)),
                ('company_info', models.TextField(blank=True, null=True)),
                ('extra_notes', models.TextField(blank=True, null=True)),
                ('script_file', models.FileField(blank=True, null=True, upload_to=core.models.random_name_contract_files)),
                ('active', models.BooleanField(default=True)),
                ('contract', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.contract')),
            ],
        ),
    ]
