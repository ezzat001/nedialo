# Generated by Django 5.0.6 on 2024-07-25 16:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_alter_profile_joining_date'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DialerList',
            new_name='ContactList',
        ),
        migrations.RenameModel(
            old_name='DialerListSource',
            new_name='ListSource',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='agents_count',
        ),
        migrations.AddField(
            model_name='campaign',
            name='agents_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='campaign',
            name='agents_rate',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='campaign',
            name='description',
            field=models.TextField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='campaign',
            name='dialer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.dialer'),
        ),
        migrations.AddField(
            model_name='campaign',
            name='first_call_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='campaign',
            name='last_call_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='campaign',
            name='weekly_hours',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='service',
            name='service_type',
            field=models.CharField(blank=True, choices=[('calling', 'Calling Service'), ('texting', 'Texting Service'), ('email', 'Email Service'), ('admin', 'Admin Service'), ('marketing', 'Marketing Service'), ('sales', 'Sales Service')], max_length=100, null=True),
        ),
    ]
