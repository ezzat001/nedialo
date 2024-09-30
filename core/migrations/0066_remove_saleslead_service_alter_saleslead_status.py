# Generated by Django 5.1.1 on 2024-09-25 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0065_remove_saleslead_handled'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='saleslead',
            name='service',
        ),
        migrations.AlterField(
            model_name='saleslead',
            name='status',
            field=models.CharField(blank=True, choices=[('follow_up', 'Follow Up'), ('scheduled_meeting', 'Scheduled Meeting'), ('no_show', 'No Show'), ('send_contract', 'To-Send Contract'), ('follow_up_landing', 'Follow Up-Landing'), ('landed', 'Landed'), ('longterm_follow_up', 'Long Term Follow Up'), ('unresponsive', 'Unresponsive'), ('not_interested', 'Not Interested'), ('archive', 'Archive')], default='followup', max_length=50, null=True),
        ),
    ]
