# Generated by Django 5.1.1 on 2024-12-24 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0139_contract_pref_submitted_alter_application_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='contractpref',
            name='above_market_perc',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='contractpref',
            name='closing_fees',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contractpref',
            name='equity',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='contractpref',
            name='listed_owner',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contractpref',
            name='lots_type',
            field=models.CharField(blank=True, choices=[('residential', 'Residential'), ('commercial', 'Commercial'), ('both', 'Residential & Commercial')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='contractpref',
            name='on_market',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contractpref',
            name='property_type_re',
            field=models.CharField(blank=True, choices=[('residential', 'Residential'), ('commercial', 'Commercial'), ('lands', 'Vacant Lands'), ('parks', 'Parks')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='contractpref',
            name='re_license',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contractpref',
            name='realtor_fees',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contractpref',
            name='remodeled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contractpref',
            name='res_type',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]
