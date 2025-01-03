# Generated by Django 5.1.1 on 2024-10-09 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0074_affiliateprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='affiliateprofile',
            name='discovery_method',
            field=models.CharField(blank=True, choices=[('affiliate', 'Affiliate'), ('facebook', 'Facebook'), ('instagram', 'Instagram'), ('batchservice', 'Batchservice'), ('linkedin', 'Linkedin'), ('upwork', 'Upwork or other freelancing sites'), ('google_search', 'Google Search'), ('google_ads', 'Google Ads'), ('twitter', 'Twitter'), ('youtube', 'YouTube'), ('tiktok', 'TikTok'), ('pinterest', 'Pinterest'), ('referral', 'Referral from a Friend'), ('email_newsletter', 'Email Newsletter'), ('outreach_call', 'Outreach Representative Calls')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='clientprofile',
            name='discovery_method',
            field=models.CharField(blank=True, choices=[('affiliate', 'Affiliate'), ('facebook', 'Facebook'), ('instagram', 'Instagram'), ('batchservice', 'Batchservice'), ('linkedin', 'Linkedin'), ('upwork', 'Upwork or other freelancing sites'), ('google_search', 'Google Search'), ('google_ads', 'Google Ads'), ('twitter', 'Twitter'), ('youtube', 'YouTube'), ('tiktok', 'TikTok'), ('pinterest', 'Pinterest'), ('referral', 'Referral from a Friend'), ('email_newsletter', 'Email Newsletter'), ('outreach_call', 'Outreach Representative Calls')], max_length=20, null=True),
        ),
    ]
