# Generated by Django 5.1.1 on 2024-10-11 19:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0083_feedback_feedback_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedback',
            name='positive',
        ),
    ]