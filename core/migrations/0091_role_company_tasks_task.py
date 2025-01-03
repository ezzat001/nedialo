# Generated by Django 5.1.1 on 2024-10-21 21:04

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0090_campaign_lookerstudio'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='role',
            name='company_tasks',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('due', models.DateTimeField(blank=True, null=True)),
                ('completed', models.DateTimeField(blank=True, null=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('priority', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=1)),
                ('executive_dep', models.BooleanField(default=False)),
                ('ops_dep', models.BooleanField(default=False)),
                ('data_dep', models.BooleanField(default=False)),
                ('workforce_dep', models.BooleanField(default=False)),
                ('quality_dep', models.BooleanField(default=False)),
                ('dev_dep', models.BooleanField(default=False)),
                ('sales_dep', models.BooleanField(default=False)),
                ('hr_dep', models.BooleanField(default=False)),
                ('assigned', models.CharField(blank=True, choices=[('executive_dep', 'Executive Management'), ('ops_dep', 'Operations Management'), ('data_dep', 'Data Management'), ('workforce_dep', 'Workforce'), ('quality_dep', 'Quality'), ('dev_dep', 'Development'), ('sales_dep', 'Sales'), ('hr_dep', 'Human Resources')], max_length=50, null=True)),
                ('status', models.CharField(blank=True, choices=[('in_progress', 'In Progress'), ('on_hold', 'On Hold'), ('blocked', 'Blocked'), ('cancelled', 'Cancelled'), ('completed', 'Completed')], default='in_progress', max_length=50, null=True)),
                ('active', models.BooleanField(default=True)),
                ('agent_profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='task_agent_profile', to='core.profile')),
                ('agent_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='task_agent_user', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='task_modified_by', to='core.profile')),
            ],
        ),
    ]
