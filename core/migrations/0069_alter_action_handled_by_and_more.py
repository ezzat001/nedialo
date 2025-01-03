# Generated by Django 5.1.1 on 2024-09-27 15:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0068_remove_profile_assigned_campaign'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='handled_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='handled_by_deduction', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='campaigndisposetting',
            name='campaign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='camp_dispo', to='core.campaign'),
        ),
        migrations.AlterField(
            model_name='leadhandlingsettings',
            name='campaign',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.campaign'),
        ),
        migrations.AlterField(
            model_name='leave',
            name='agent_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leave_profile', to='core.profile'),
        ),
        migrations.AlterField(
            model_name='leave',
            name='agent_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='leave_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='leave',
            name='handled_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='handled_by_leave', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='leave',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='team_leave', to='core.team'),
        ),
        migrations.AlterField(
            model_name='prepayment',
            name='handled_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='handled_by_prepayment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='seatassignmentlog',
            name='agent_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.profile'),
        ),
        migrations.AlterField(
            model_name='seatassignmentlog',
            name='dialer_credentials',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.dialercredentials'),
        ),
        migrations.AlterField(
            model_name='workstatus',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
