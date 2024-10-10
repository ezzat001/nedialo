# Generated by Django 5.1.1 on 2024-10-09 14:24

import core.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0073_role_admin_affiliates'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AffiliateProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('picture', models.ImageField(blank=True, null=True, upload_to=core.models.random_name_profile_pic)),
                ('full_name', models.CharField(blank=True, max_length=50, null=True)),
                ('password', models.CharField(blank=True, max_length=50, null=True)),
                ('joining_date', models.DateField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=50, null=True)),
                ('state', models.CharField(blank=True, choices=[('ak', 'Alaska'), ('al', 'Alabama'), ('ar', 'Arkansas'), ('as', 'American Samoa'), ('az', 'Arizona'), ('ca', 'California'), ('co', 'Colorado'), ('ct', 'Connecticut'), ('dc', 'District of Columbia'), ('de', 'Delaware'), ('fl', 'Florida'), ('ga', 'Georgia'), ('gu', 'Guam'), ('hi', 'Hawaii'), ('ia', 'Iowa'), ('id', 'Idaho'), ('il', 'Illinois'), ('in', 'Indiana'), ('ks', 'Kansas'), ('ky', 'Kentucky'), ('la', 'Louisiana'), ('ma', 'Massachusetts'), ('md', 'Maryland'), ('me', 'Maine'), ('mi', 'Michigan'), ('mn', 'Minnesota'), ('mo', 'Missouri'), ('ms', 'Mississippi'), ('mt', 'Montana'), ('nc', 'North Carolina'), ('nd', 'North Dakota'), ('ne', 'Nebraska'), ('nh', 'New Hampshire'), ('nj', 'New Jersey'), ('nm', 'New Mexico'), ('nv', 'Nevada'), ('ny', 'New York'), ('oh', 'Ohio'), ('ok', 'Oklahoma'), ('or', 'Oregon'), ('pa', 'Pennsylvania'), ('pr', 'Puerto Rico'), ('ri', 'Rhode Island'), ('sc', 'South Carolina'), ('sd', 'South Dakota'), ('tn', 'Tennessee'), ('tx', 'Texas'), ('ut', 'Utah'), ('va', 'Virginia'), ('vi', 'Virgin Islands'), ('vt', 'Vermont'), ('wa', 'Washington'), ('wi', 'Wisconsin'), ('wv', 'West Virginia'), ('wy', 'Wyoming')], max_length=50, null=True)),
                ('client_status', models.CharField(blank=True, choices=[('active', 'Active'), ('hold', 'Hold'), ('pending', 'Pending'), ('inactive', 'Inactive')], default='active', max_length=50, null=True)),
                ('discovery_method', models.CharField(blank=True, choices=[('facebook', 'Facebook'), ('instagram', 'Instagram'), ('batchservice', 'Batchservice'), ('linkedin', 'Linkedin'), ('upwork', 'Upwork or other freelancing sites'), ('google_search', 'Google Search'), ('google_ads', 'Google Ads'), ('twitter', 'Twitter'), ('youtube', 'YouTube'), ('tiktok', 'TikTok'), ('pinterest', 'Pinterest'), ('referral', 'Referral from a Friend'), ('email_newsletter', 'Email Newsletter'), ('outreach_call', 'Outreach Representative Calls')], max_length=20, null=True)),
                ('settings_theme', models.CharField(choices=[('white', 'White'), ('dark', 'Dark')], default='white', max_length=50)),
                ('maps_theme', models.CharField(choices=[('white', 'White'), ('dark', 'Dark')], default='dark', max_length=50)),
                ('active', models.BooleanField(default=True)),
                ('role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='affiliate_profile_role', to='core.role')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]