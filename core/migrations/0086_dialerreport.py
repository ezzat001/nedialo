# Generated by Django 5.1.1 on 2024-10-16 13:32

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0085_role_dialer_reports'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DialerReport',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dialer', models.CharField(blank=True, choices=[('batchdialer', 'Batch Dialer'), ('calltools', 'Call Tools')], max_length=50, null=True)),
                ('api_key', models.TextField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('campaign', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.campaign')),
                ('client_profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.clientprofile')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
