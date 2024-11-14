# Generated by Django 5.1.1 on 2024-11-14 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0105_remove_application_skills_delete_applicationskill_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaign',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='profile',
            name='status',
            field=models.CharField(blank=True, choices=[('active', 'Active'), ('upl', 'UPL'), ('annual', 'Annual'), ('casual', 'Casual'), ('sick', 'Sick'), ('hold', 'Hold'), ('dropped', 'Dropped'), ('blacklisted', 'Blacklisted')], default='active', max_length=20, null=True),
        ),
    ]