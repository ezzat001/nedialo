# Generated by Django 5.1.1 on 2024-09-17 18:05

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0056_prepayment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prepayment',
            name='agent_name',
        ),
        migrations.AddField(
            model_name='prepayment',
            name='agent_profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='agent_profile_prepayment', to='core.profile'),
        ),
        migrations.AlterField(
            model_name='prepayment',
            name='agent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='prepayment',
            name='submission_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]