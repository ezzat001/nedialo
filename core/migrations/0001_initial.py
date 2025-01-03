# Generated by Django 5.0.6 on 2024-08-06 19:16

import core.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField(blank=True, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('agents_count', models.PositiveIntegerField(default=0)),
                ('agents_rate', models.PositiveIntegerField(default=0)),
                ('weekly_hours', models.PositiveIntegerField(default=0)),
                ('campaign_type', models.CharField(blank=True, choices=[('calling', 'Calling Service'), ('texting', 'Texting Service'), ('email', 'Email Service'), ('admin', 'Admin Service'), ('marketing', 'Marketing Service'), ('sales', 'Sales Service')], max_length=50, null=True)),
                ('lead_points', models.PositiveIntegerField(default=0)),
                ('status', models.CharField(blank=True, choices=[('active', 'Active'), ('hold', 'Hold'), ('pending', 'Pending'), ('inactive', 'Inactive')], default='active', max_length=50, null=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='DataSource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('source_type', models.CharField(blank=True, choices=[('pulling', 'List Pulling'), ('skip_tracing', 'Skip Tracing'), ('skip_pull', 'List Pulling & Skip Tracing'), ('data_management', 'Data Management'), ('crm', 'CRM')], max_length=50, null=True)),
                ('data_source', models.BooleanField(default=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Dialer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('dialer_type', models.CharField(blank=True, choices=[('calling', 'Calling'), ('texting', 'Texting')], max_length=50, null=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role_name', models.CharField(blank=True, max_length=50, null=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ServerSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=50)),
                ('company_website', models.URLField(blank=True, null=True)),
                ('logo_main', models.ImageField(blank=True, null=True, upload_to='server_settings')),
                ('logo_login', models.ImageField(blank=True, null=True, upload_to='server_settings')),
                ('favicon', models.ImageField(blank=True, null=True, upload_to='server_settings')),
                ('logo_dashboard_width', models.CharField(blank=True, max_length=10, null=True)),
                ('logo_dashboard_height', models.CharField(blank=True, max_length=10, null=True)),
                ('facebook', models.URLField(blank=True, null=True)),
                ('instagram', models.URLField(blank=True, null=True)),
                ('linkedin', models.URLField(blank=True, null=True)),
                ('about_us', models.URLField(blank=True, null=True)),
                ('privacy', models.URLField(blank=True, null=True)),
                ('terms', models.URLField(blank=True, null=True)),
                ('hide_campaign_leadform', models.BooleanField(default=False)),
                ('hide_client_leadform', models.BooleanField(default=False)),
                ('maintenance', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('service_type', models.CharField(blank=True, choices=[('calling', 'Calling Service'), ('texting', 'Texting Service'), ('email', 'Email Service'), ('admin', 'Admin Service'), ('marketing', 'Marketing Service'), ('sales', 'Sales Service')], max_length=100, null=True)),
                ('status', models.CharField(blank=True, choices=[('active', 'Active'), ('hold', 'Hold'), ('pending', 'Pending'), ('inactive', 'Inactive')], default='active', max_length=50, null=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_name', models.CharField(blank=True, max_length=50, null=True)),
                ('team_type', models.CharField(blank=True, choices=[('callers', 'Cold Callers'), ('sales', 'Sales'), ('dispo', 'Dispositions'), ('acq', 'Acquisitions'), ('data', 'Data Management'), ('quality', 'Quality'), ('team_leaders', 'team_leaders')], max_length=50, null=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField(auto_now_add=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('position', models.CharField(blank=True, choices=[('cold_caller', 'Cold Caller'), ('acq_manager', 'Acquisition Manager'), ('dispo_manager', 'Disposition Manager'), ('data_manager', 'Data Manager'), ('sales', 'Sales')], max_length=50, null=True)),
                ('full_name', models.CharField(blank=True, max_length=50, null=True)),
                ('email', models.CharField(blank=True, max_length=50, null=True)),
                ('phone', models.CharField(blank=True, max_length=50, null=True)),
                ('education', models.CharField(blank=True, choices=[('highschool', 'High School'), ('undergraduate', 'Undergradute'), ('bachelors', 'Bachelors'), ('mba', 'MBA')], max_length=50, null=True)),
                ('experience', models.TextField(blank=True, null=True)),
                ('start_date', models.TextField(blank=True, null=True)),
                ('shift', models.CharField(blank=True, choices=[('part_time', 'Part Time'), ('full_time', 'Full Time')], max_length=50, null=True)),
                ('audio_file', models.FileField(blank=True, null=True, upload_to='applications_audio')),
                ('status', models.CharField(blank=True, choices=[('accepted', 'Accepted'), ('rejected', 'Rejected'), ('pending', 'Pending')], default='pending', max_length=50, null=True)),
                ('active', models.BooleanField(default=True)),
                ('referrer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CampaignDispoSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot1_dispo', models.CharField(blank=True, max_length=50, null=True)),
                ('slot2_dispo', models.CharField(blank=True, max_length=50, null=True)),
                ('slot3_dispo', models.CharField(blank=True, max_length=50, null=True)),
                ('slot4_dispo', models.CharField(blank=True, max_length=50, null=True)),
                ('slot5_dispo', models.CharField(blank=True, max_length=50, null=True)),
                ('slot6_dispo', models.CharField(blank=True, max_length=50, null=True)),
                ('slot7_dispo', models.CharField(blank=True, max_length=50, null=True)),
                ('slot8_dispo', models.CharField(blank=True, max_length=50, null=True)),
                ('slot9_dispo', models.CharField(blank=True, max_length=50, null=True)),
                ('slot10_dispo', models.CharField(blank=True, max_length=50, null=True)),
                ('slot11_dispo', models.CharField(blank=True, max_length=50, null=True)),
                ('slot12_dispo', models.CharField(blank=True, max_length=50, null=True)),
                ('slot13_dispo', models.CharField(blank=True, max_length=50, null=True)),
                ('slot14_dispo', models.CharField(blank=True, max_length=50, null=True)),
                ('slot15_dispo', models.CharField(blank=True, max_length=50, null=True)),
                ('active', models.BooleanField(default=True)),
                ('campaign', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='camp_dispo', to='core.campaign')),
            ],
        ),
        migrations.CreateModel(
            name='ContactList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('contacts', models.IntegerField(blank=True, null=True)),
                ('states', models.TextField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('pulled', 'Pulled'), ('being_dialed', 'Being Dialed'), ('paused', 'Paused'), ('dialed', 'Dialed')], max_length=50, null=True)),
                ('active', models.BooleanField(default=True)),
                ('campaign', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='list_campaign', to='core.campaign')),
                ('skip_tracing', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='skiptracing_list', to='core.datasource')),
                ('source', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='datasource_list', to='core.datasource')),
                ('dialer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.dialer')),
            ],
        ),
        migrations.CreateModel(
            name='ContactListPerformance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField(blank=True, null=True)),
                ('date', models.DateField(blank=True, null=True)),
                ('dispo_count', models.IntegerField(blank=True, default=0, null=True)),
                ('active', models.BooleanField(default=True)),
                ('campaign', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='performance_camp', to='core.contactlist')),
                ('dialer_list', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='performance_list', to='core.contactlist')),
                ('dispo', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='performance_dispos', to='core.campaigndisposetting')),
            ],
        ),
        migrations.AddField(
            model_name='campaign',
            name='datasources',
            field=models.ManyToManyField(blank=True, related_name='datasources_campaign', to='core.datasource'),
        ),
        migrations.CreateModel(
            name='DataSourceCredentials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_type', models.CharField(blank=True, choices=[('full_access', 'Full Access'), ('limited_access', 'Limited Access')], max_length=50, null=True)),
                ('username', models.CharField(blank=True, max_length=50, null=True)),
                ('password', models.CharField(blank=True, max_length=50, null=True)),
                ('active', models.BooleanField(default=True)),
                ('campaign', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.campaign')),
                ('datasource', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.datasource')),
            ],
        ),
        migrations.AddField(
            model_name='campaign',
            name='dialer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.dialer'),
        ),
        migrations.CreateModel(
            name='DialerCredentials',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_type', models.CharField(blank=True, choices=[('agent', 'Agent'), ('supervisor', 'Supervisor'), ('admin', 'Admin')], max_length=50, null=True)),
                ('username', models.CharField(blank=True, max_length=50, null=True)),
                ('password', models.CharField(blank=True, max_length=50, null=True)),
                ('active', models.BooleanField(default=True)),
                ('campaign', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.campaign')),
                ('dialer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.dialer')),
            ],
        ),
        migrations.CreateModel(
            name='LeadHandlingSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slot1_name', models.CharField(blank=True, max_length=100, null=True)),
                ('slot1_percentage', models.FloatField(default=0)),
                ('slot2_name', models.CharField(blank=True, max_length=100, null=True)),
                ('slot2_percentage', models.FloatField(default=0)),
                ('slot3_name', models.CharField(blank=True, max_length=100, null=True)),
                ('slot3_percentage', models.FloatField(default=0)),
                ('slot4_name', models.CharField(blank=True, max_length=100, null=True)),
                ('slot4_percentage', models.FloatField(default=0)),
                ('slot5_name', models.CharField(blank=True, max_length=100, null=True)),
                ('slot5_percentage', models.FloatField(default=0)),
                ('slot6_name', models.CharField(blank=True, max_length=100, null=True)),
                ('slot6_percentage', models.FloatField(default=0)),
                ('slot7_name', models.CharField(blank=True, max_length=100, null=True)),
                ('slot7_percentage', models.FloatField(default=0)),
                ('slot8_name', models.CharField(blank=True, max_length=100, null=True)),
                ('slot8_percentage', models.FloatField(default=0)),
                ('slot9_name', models.CharField(blank=True, max_length=100, null=True)),
                ('slot9_percentage', models.FloatField(default=0)),
                ('slot10_name', models.CharField(blank=True, max_length=100, null=True)),
                ('slot10_percentage', models.FloatField(default=0)),
                ('activated', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True)),
                ('campaign', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.campaign')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('picture', models.ImageField(blank=True, null=True, upload_to=core.models.random_name_profile_pic)),
                ('full_name', models.CharField(blank=True, max_length=50, null=True)),
                ('password', models.CharField(blank=True, max_length=50, null=True)),
                ('phone_name', models.CharField(blank=True, max_length=50, null=True)),
                ('hiring_date', models.DateField(blank=True, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('login_time', models.TimeField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('status', models.CharField(blank=True, choices=[('active', 'Active'), ('upl', 'UPL'), ('annual', 'Annual'), ('casual', 'Casual'), ('sick', 'Sick'), ('inactive', 'Inactive'), ('dropped', 'Dropped'), ('blacklisted', 'Blacklisted')], default='active', max_length=20, null=True)),
                ('dialer_user', models.CharField(blank=True, max_length=40, null=True)),
                ('dialer_password', models.CharField(blank=True, max_length=40, null=True)),
                ('hourly_rate', models.FloatField(blank=True, null=True)),
                ('monthly_salary', models.FloatField(blank=True, null=True)),
                ('salary_type', models.CharField(blank=True, choices=[('monthly', 'Monthly'), ('hourly', 'Hourly')], max_length=20, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=50, null=True)),
                ('residence', models.CharField(blank=True, choices=[('af', 'Afghanistan'), ('al', 'Albania'), ('dz', 'Algeria'), ('as', 'American Samoa'), ('ad', 'Andorra'), ('ao', 'Angola'), ('ai', 'Anguilla'), ('aq', 'Antarctica'), ('ag', 'Antigua and Barbuda'), ('ar', 'Argentina'), ('am', 'Armenia'), ('aw', 'Aruba'), ('au', 'Australia'), ('at', 'Austria'), ('az', 'Azerbaijan'), ('bs', 'Bahamas'), ('bh', 'Bahrain'), ('bd', 'Bangladesh'), ('bb', 'Barbados'), ('by', 'Belarus'), ('be', 'Belgium'), ('bz', 'Belize'), ('bj', 'Benin'), ('bm', 'Bermuda'), ('bt', 'Bhutan'), ('bo', 'Bolivia'), ('bq', 'Bonaire, Sint Eustatius and Saba'), ('ba', 'Bosnia and Herzegovina'), ('bw', 'Botswana'), ('bv', 'Bouvet Island'), ('br', 'Brazil'), ('io', 'British Indian Ocean Territory'), ('bn', 'Brunei Darussalam'), ('bg', 'Bulgaria'), ('bf', 'Burkina Faso'), ('bi', 'Burundi'), ('cv', 'Cabo Verde'), ('kh', 'Cambodia'), ('cm', 'Cameroon'), ('ca', 'Canada'), ('ky', 'Cayman Islands'), ('cf', 'Central African Republic'), ('td', 'Chad'), ('cl', 'Chile'), ('cn', 'China'), ('cx', 'Christmas Island'), ('cc', 'Cocos (Keeling) Islands'), ('co', 'Colombia'), ('km', 'Comoros'), ('cg', 'Congo'), ('cd', 'Congo, Democratic Republic of the'), ('ck', 'Cook Islands'), ('cr', 'Costa Rica'), ('ci', "Côte d'Ivoire"), ('hr', 'Croatia'), ('cu', 'Cuba'), ('cw', 'Curaçao'), ('cy', 'Cyprus'), ('cz', 'Czechia'), ('dk', 'Denmark'), ('dj', 'Djibouti'), ('dm', 'Dominica'), ('do', 'Dominican Republic'), ('ec', 'Ecuador'), ('eg', 'Egypt'), ('sv', 'El Salvador'), ('gq', 'Equatorial Guinea'), ('er', 'Eritrea'), ('ee', 'Estonia'), ('sz', 'Eswatini'), ('et', 'Ethiopia'), ('fk', 'Falkland Islands (Malvinas)'), ('fo', 'Faroe Islands'), ('fj', 'Fiji'), ('fi', 'Finland'), ('fr', 'France'), ('gf', 'French Guiana'), ('pf', 'French Polynesia'), ('tf', 'French Southern Territories'), ('ga', 'Gabon'), ('gm', 'Gambia'), ('ge', 'Georgia'), ('de', 'Germany'), ('gh', 'Ghana'), ('gi', 'Gibraltar'), ('gr', 'Greece'), ('gl', 'Greenland'), ('gd', 'Grenada'), ('gp', 'Guadeloupe'), ('gu', 'Guam'), ('gt', 'Guatemala'), ('gg', 'Guernsey'), ('gn', 'Guinea'), ('gw', 'Guinea-Bissau'), ('gy', 'Guyana'), ('ht', 'Haiti'), ('hm', 'Heard Island and McDonald Islands'), ('va', 'Holy See'), ('hn', 'Honduras'), ('hk', 'Hong Kong'), ('hu', 'Hungary'), ('is', 'Iceland'), ('in', 'India'), ('id', 'Indonesia'), ('ir', 'Iran (Islamic Republic of)'), ('iq', 'Iraq'), ('ie', 'Ireland'), ('im', 'Isle of Man'), ('il', 'Israel'), ('it', 'Italy'), ('jm', 'Jamaica'), ('jp', 'Japan'), ('je', 'Jersey'), ('jo', 'Jordan'), ('kz', 'Kazakhstan'), ('ke', 'Kenya'), ('ki', 'Kiribati'), ('kp', "Korea (Democratic People's Republic of)"), ('kr', 'Korea, Republic of'), ('kw', 'Kuwait'), ('kg', 'Kyrgyzstan'), ('la', "Lao People's Democratic Republic"), ('lv', 'Latvia'), ('lb', 'Lebanon'), ('ls', 'Lesotho'), ('lr', 'Liberia'), ('ly', 'Libya'), ('li', 'Liechtenstein'), ('lt', 'Lithuania'), ('lu', 'Luxembourg'), ('mo', 'Macao'), ('mg', 'Madagascar'), ('mw', 'Malawi'), ('my', 'Malaysia'), ('mv', 'Maldives'), ('ml', 'Mali'), ('mt', 'Malta'), ('mh', 'Marshall Islands'), ('mq', 'Martinique'), ('mr', 'Mauritania'), ('mu', 'Mauritius'), ('yt', 'Mayotte'), ('mx', 'Mexico'), ('fm', 'Micronesia (Federated States of)'), ('md', 'Moldova (Republic of)'), ('mc', 'Monaco'), ('mn', 'Mongolia'), ('me', 'Montenegro'), ('ms', 'Montserrat'), ('ma', 'Morocco'), ('mz', 'Mozambique'), ('mm', 'Myanmar'), ('na', 'Namibia'), ('nr', 'Nauru'), ('np', 'Nepal'), ('nl', 'Netherlands'), ('nc', 'New Caledonia'), ('nz', 'New Zealand'), ('ni', 'Nicaragua'), ('ne', 'Niger'), ('ng', 'Nigeria'), ('nu', 'Niue'), ('nf', 'Norfolk Island'), ('mp', 'Northern Mariana Islands'), ('no', 'Norway'), ('om', 'Oman'), ('pk', 'Pakistan'), ('pw', 'Palau'), ('ps', 'Palestine, State of'), ('pa', 'Panama'), ('pg', 'Papua New Guinea'), ('py', 'Paraguay'), ('pe', 'Peru'), ('ph', 'Philippines'), ('pn', 'Pitcairn'), ('pl', 'Poland'), ('pt', 'Portugal'), ('pr', 'Puerto Rico'), ('qa', 'Qatar'), ('mk', 'Republic of North Macedonia'), ('ro', 'Romania'), ('ru', 'Russian Federation'), ('rw', 'Rwanda'), ('re', 'Réunion'), ('bl', 'Saint Barthélemy'), ('sh', 'Saint Helena, Ascension and Tristan da Cunha'), ('kn', 'Saint Kitts and Nevis'), ('lc', 'Saint Lucia'), ('mf', 'Saint Martin (French part)'), ('pm', 'Saint Pierre and Miquelon'), ('vc', 'Saint Vincent and the Grenadines'), ('ws', 'Samoa'), ('sm', 'San Marino'), ('st', 'Sao Tome and Principe'), ('sa', 'Saudi Arabia'), ('sn', 'Senegal'), ('rs', 'Serbia'), ('sc', 'Seychelles'), ('sl', 'Sierra Leone'), ('sg', 'Singapore'), ('sx', 'Sint Maarten (Dutch part)'), ('sk', 'Slovakia'), ('si', 'Slovenia'), ('sb', 'Solomon Islands'), ('so', 'Somalia'), ('za', 'South Africa'), ('gs', 'South Georgia and the South Sandwich Islands'), ('ss', 'South Sudan'), ('es', 'Spain'), ('lk', 'Sri Lanka'), ('sd', 'Sudan'), ('sr', 'Suriname'), ('sj', 'Svalbard and Jan Mayen'), ('se', 'Sweden'), ('ch', 'Switzerland'), ('sy', 'Syrian Arab Republic'), ('tw', 'Taiwan, Province of China'), ('tj', 'Tajikistan'), ('tz', 'Tanzania, United Republic of'), ('th', 'Thailand'), ('tl', 'Timor-Leste'), ('tg', 'Togo'), ('tk', 'Tokelau'), ('to', 'Tonga'), ('tt', 'Trinidad and Tobago'), ('tn', 'Tunisia'), ('tr', 'Turkey'), ('tm', 'Turkmenistan'), ('tc', 'Turks and Caicos Islands'), ('tv', 'Tuvalu'), ('ug', 'Uganda'), ('ua', 'Ukraine'), ('ae', 'United Arab Emirates'), ('gb', 'United Kingdom of Great Britain and Northern Ireland'), ('us', 'United States of America'), ('um', 'United States Minor Outlying Islands'), ('uy', 'Uruguay'), ('uz', 'Uzbekistan'), ('vu', 'Vanuatu'), ('ve', 'Venezuela (Bolivarian Republic of)'), ('vn', 'Viet Nam'), ('vg', 'Virgin Islands (British)'), ('vi', 'Virgin Islands (U.S.)'), ('wf', 'Wallis and Futuna'), ('eh', 'Western Sahara'), ('ye', 'Yemen'), ('zm', 'Zambia'), ('zw', 'Zimbabwe')], max_length=50, null=True)),
                ('state', models.CharField(blank=True, choices=[('ak', 'Alaska'), ('al', 'Alabama'), ('ar', 'Arkansas'), ('as', 'American Samoa'), ('az', 'Arizona'), ('ca', 'California'), ('co', 'Colorado'), ('ct', 'Connecticut'), ('dc', 'District of Columbia'), ('de', 'Delaware'), ('fl', 'Florida'), ('ga', 'Georgia'), ('gu', 'Guam'), ('hi', 'Hawaii'), ('ia', 'Iowa'), ('id', 'Idaho'), ('il', 'Illinois'), ('in', 'Indiana'), ('ks', 'Kansas'), ('ky', 'Kentucky'), ('la', 'Louisiana'), ('ma', 'Massachusetts'), ('md', 'Maryland'), ('me', 'Maine'), ('mi', 'Michigan'), ('mn', 'Minnesota'), ('mo', 'Missouri'), ('ms', 'Mississippi'), ('mt', 'Montana'), ('nc', 'North Carolina'), ('nd', 'North Dakota'), ('ne', 'Nebraska'), ('nh', 'New Hampshire'), ('nj', 'New Jersey'), ('nm', 'New Mexico'), ('nv', 'Nevada'), ('ny', 'New York'), ('oh', 'Ohio'), ('ok', 'Oklahoma'), ('or', 'Oregon'), ('pa', 'Pennsylvania'), ('pr', 'Puerto Rico'), ('ri', 'Rhode Island'), ('sc', 'South Carolina'), ('sd', 'South Dakota'), ('tn', 'Tennessee'), ('tx', 'Texas'), ('ut', 'Utah'), ('va', 'Virginia'), ('vi', 'Virgin Islands'), ('vt', 'Vermont'), ('wa', 'Washington'), ('wi', 'Wisconsin'), ('wv', 'West Virginia'), ('wy', 'Wyoming')], max_length=50, null=True)),
                ('joining_date', models.DateField(blank=True, null=True)),
                ('client_status', models.CharField(blank=True, choices=[('active', 'Active'), ('hold', 'Hold'), ('pending', 'Pending'), ('inactive', 'Inactive')], default='active', max_length=50, null=True)),
                ('discovery_method', models.CharField(blank=True, choices=[('facebook', 'Facebook'), ('instagram', 'Instagram'), ('batchservice', 'Batchservice'), ('linkedin', 'Linkedin'), ('upwork', 'Upwork or other freelancing sites'), ('google_search', 'Google Search'), ('google_ads', 'Google Ads'), ('twitter', 'Twitter'), ('youtube', 'YouTube'), ('tiktok', 'TikTok'), ('pinterest', 'Pinterest'), ('referral', 'Referral from a Friend'), ('email_newsletter', 'Email Newsletter'), ('outreach_call', 'Outreach Representative Calls')], max_length=20, null=True)),
                ('discord', models.CharField(blank=True, max_length=100, null=True)),
                ('payoneer', models.CharField(blank=True, max_length=100, null=True)),
                ('instapay', models.CharField(blank=True, max_length=100, null=True)),
                ('payment_method', models.CharField(choices=[('payoneer', 'Payoneer'), ('instapay', 'InstaPay')], default='payoneer', max_length=50)),
                ('national_id', models.ImageField(blank=True, null=True, upload_to=core.models.random_name_national_id)),
                ('settings_theme', models.CharField(choices=[('white', 'White'), ('dark', 'Dark')], default='white', max_length=50)),
                ('maps_theme', models.CharField(choices=[('white', 'White'), ('dark', 'Dark')], default='white', max_length=50)),
                ('active', models.BooleanField(default=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('role', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='profile_role', to='core.role')),
                ('services', models.ManyToManyField(blank=True, related_name='client_services', to='core.service')),
                ('team', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.team')),
            ],
        ),
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('pushed_time', models.TimeField(auto_now_add=True)),
                ('pushed_date', models.DateField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('lead_id', models.PositiveIntegerField(primary_key=True, serialize=False, unique=True)),
                ('property_type', models.CharField(blank=True, choices=[('house', 'House'), ('vacant_land', 'Vacant Land'), ('business', 'Business'), ('apartment', 'Apartment'), ('codo', 'Condo'), ('mobile_home', 'Mobile Home')], default='house', max_length=50, null=True)),
                ('lead_status', models.CharField(blank=True, choices=[('pending', 'Pending'), ('qualified', 'Qualified'), ('disqualified', 'Disqualified'), ('callback', 'Callback'), ('duplicate', 'Duplicate'), ('invaild', 'Invalid')], default='pending', max_length=50, null=True)),
                ('seller_name', models.CharField(blank=True, max_length=50, null=True)),
                ('seller_phone', models.CharField(blank=True, max_length=50, null=True)),
                ('seller_email', models.CharField(blank=True, max_length=50, null=True)),
                ('timeline', models.CharField(blank=True, choices=[('two_weeks', '2 Weeks'), ('one_month', '1 Month'), ('two_month', '2 Month'), ('three_month', '3 Month'), ('four_month', '4 Month'), ('five_month', '5 Month'), ('six_month', '6 Month'), ('more_than_six_month', '+6 Month')], default='two_weeks', max_length=50, null=True)),
                ('reason', models.TextField(blank=True, null=True)),
                ('property_address', models.TextField(blank=True, null=True)),
                ('asking_price', models.CharField(blank=True, max_length=50, null=True)),
                ('market_value', models.CharField(blank=True, max_length=50, null=True)),
                ('general_info', models.TextField(blank=True, null=True)),
                ('property_url', models.TextField(blank=True, null=True)),
                ('callback', models.CharField(blank=True, max_length=50, null=True)),
                ('extra_notes', models.TextField(blank=True, null=True)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('quality_notes', models.TextField(blank=True, null=True)),
                ('quality_to_agent_notes', models.TextField(blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('agent_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('campaign', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lead_campaign', to='core.campaign')),
                ('contact_list', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lead_list', to='core.contactlist')),
                ('handled_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='handled_by_lead_post', to=settings.AUTH_USER_MODEL)),
                ('agent_profile', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lead_profile', to='core.profile')),
            ],
        ),
        migrations.AddField(
            model_name='campaign',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.profile'),
        ),
    ]
