# Generated by Django 5.1.1 on 2024-09-19 04:37

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0060_application_handled_by'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ManualHours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('hours', models.IntegerField(blank=True, null=True)),
                ('positive', models.BooleanField(default=True)),
                ('reason', models.CharField(blank=True, max_length=200, null=True)),
                ('active', models.BooleanField(default=True)),
                ('admin_profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='admin_profile_hours', to='core.profile')),
                ('admin_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='admin_user_hours', to=settings.AUTH_USER_MODEL)),
                ('agent_profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='agent_profile_hours', to='core.profile')),
                ('agent_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='agent_user_hours', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
