# Generated by Django 5.1.1 on 2024-10-21 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0089_role_client_campaign_performance_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='campaign',
            name='lookerstudio',
            field=models.TextField(blank=True, null=True),
        ),
    ]