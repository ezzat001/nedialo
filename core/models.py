from django.db import models
from django.contrib.auth.models import User
from nedialo.constants import US_STATES_CHOICES,COUNTRIES_CHOICES
from django.template.defaultfilters import slugify  # new
from django.urls import reverse
from django.utils import timezone
import os,uuid

STATUS_CHOICES = (
    ('active','Active'),
    ('upl', 'UPL'),
    ('annual','Annual'),
    ('casual','Casual'),
    ('sick','Sick'),
    ('inactive','Inactive'),
    ('dropped','Dropped'),
    ('blacklisted','Blacklisted'),
)

THEME_CHOICES = (
    ("white","White"),
    ("dark","Dark"),
)

PAYMENT_CHOICES = (
    ("payoneer","Payoneer"),
    ("instapay","InstaPay"),
)


TEAM_TYPES = (
    ('callers', 'Cold Callers'),
    ('sales', 'Sales'),
    ('dispo', 'Dispositions'),
    ('acq', 'Acquisitions'),
    ('data', 'Data Management'),
    ('quality', 'Quality'),
    ('team_leaders', 'team_leaders'),
)

APPLICATION_POS_CHOICES = (
    ("cold_caller", "Cold Caller"),
    ("acq_manager", "Acquisition Manager"),
    ("dispo_manager","Disposition Manager"),
    ("data_manager","Data Manager"),
    ('sales', "Sales")

)

APPLICATION_EDU_CHOICES = (
    ("highschool", "High School"),
    ("undergraduate", "Undergradute"),
    ("bachelors","Bachelors"),
    ("mba","MBA"),

)

APPLICATION_SHIFT_CHOICES = (
    ("part_time", "Part Time"),
    ("full_time","Full Time"),

)


APPLICATION_STATUS_CHOICES = (
    ('accepted','Accepted'),
    ('rejected', 'Rejected'),
    ('pending', 'Pending'),
)


LEAD_CHOICES = (
    ('pending','Pending'),
    ('qualified', 'Qualified'),
    ('disqualified','Disqualified'),
    ('callback', 'Callback'),
    ('duplicate', 'Duplicate'),
    ('invaild','Invalid'),
   
)

PROPERTY_CHOICES = (
    ('house','House'),
    ('vacant_land','Vacant Land'),
    ('business', 'Business'),
    ('apartment', 'Apartment'),
    ('codo', 'Condo'),
    ('mobile_home','Mobile Home'),
)

TIMELINE_CHOICES = (
    ('two_weeks', "2 Weeks"),
    ('one_month', "1 Month"),
    ('two_month', "2 Month"),
    ('three_month', "3 Month"),
    ('four_month', "4 Month"),
    ('five_month', "5 Month"),
    ('six_month', "6 Month"),
    ('more_than_six_month', "+6 Month"),



)


CAMP_ACTIVITY = (
    ('active', 'Active'),
    ('hold', 'Hold'),
    ('pending','Pending'),
    ('inactive', 'Inactive'),
)

SALARY_TYPE = (
    ('monthly','Monthly'),
    ('hourly', 'Hourly'),
)

DISCOVERY_TYPE = (
    ("facebook", "Facebook"),
    ("instagram", "Instagram"),
    ("batchservice", "Batchservice"),
    ("linkedin", "Linkedin"),
    ("upwork", "Upwork or other freelancing sites"),
    ("google_search", "Google Search"),
    ("google_ads", "Google Ads"),
    ("twitter", "Twitter"),
    ("youtube", "YouTube"),
    ("tiktok", "TikTok"),
    ("pinterest", "Pinterest"),
    ("referral", "Referral from a Friend"),
    ("email_newsletter", "Email Newsletter"),
    ("outreach_call", "Outreach Representative Calls")
)

SERVICE_TYPES = (
    ('calling','Calling Service'),
    ('texting', 'Texting Service'),
    ('email', 'Email Service'),
    ('admin', 'Admin Service'),
    ('marketing', 'Marketing Service'),
    ('sales', 'Sales Service'),
)

DIALER_TYPES = (
    ('calling','Calling'),
    ('texting','Texting'),
)


DATASOURCE_TYPES = (
    ('pulling',"List Pulling"),
    ('skip_tracing', "Skip Tracing"),
    ('skip_pull', 'List Pulling & Skip Tracing'),
)


class ServerSetting(models.Model):
    
    company_name = models.CharField(max_length=50)
    company_website = models.URLField(null=True,blank=True)
    logo_main = models.ImageField(upload_to="server_settings",null=True,blank=True)
    logo_login = models.ImageField(upload_to="server_settings",null=True,blank=True)
    favicon = models.ImageField(upload_to="server_settings",null=True,blank=True)

    logo_dashboard_width = models.CharField(max_length=10,null=True,blank=True)
    logo_dashboard_height = models.CharField(max_length=10,null=True,blank=True)




    facebook = models.URLField(null=True,blank=True)
    instagram = models.URLField(null=True,blank=True)
    linkedin = models.URLField(null=True,blank=True)
    about_us = models.URLField(null=True,blank=True)
    privacy = models.URLField(null=True, blank=True)

    terms = models.URLField(null=True, blank=True)


    hide_campaign_leadform = models.BooleanField(default=False)
    hide_client_leadform = models.BooleanField(default=False)
    maintenance = models.BooleanField(default=False)

class Role(models.Model):
    role_name = models.CharField(max_length=50, null=True, blank=True)

    active=models.BooleanField(default=True)

    def __str__(self):
        return str(self.role_name)


class Application(models.Model):
    time = models.TimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    position = models.CharField(max_length=50, choices=APPLICATION_POS_CHOICES, null=True, blank=True)
    full_name = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    education = models.CharField(max_length=50, choices=APPLICATION_EDU_CHOICES,null=True, blank=True)
    experience = models.TextField(null=True, blank=True)
    start_date = models.TextField(null=True, blank=True)
    shift = models.CharField(max_length=50, choices=APPLICATION_SHIFT_CHOICES,null=True, blank=True)
    audio_file = models.FileField(upload_to='applications_audio', blank=True, null=True)
    status = models.CharField(max_length=50, choices=APPLICATION_STATUS_CHOICES, blank=True, null=True,default="pending")
    active = models.BooleanField(default=True)

class Team(models.Model):
    team_name = models.CharField(max_length=50, null=True, blank=True)
    team_type = models.CharField(max_length=50, choices=TEAM_TYPES, blank=True, null=True)
    active = models.BooleanField(default=True)

def random_name_national_id(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('national_ids/', filename)


def random_name_profile_pic(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'
    return os.path.join('profile_images/', filename)


class Service(models.Model): #Company Provided Services
    name = models.CharField(max_length=100)
    service_type = models.CharField(max_length=100, choices=SERVICE_TYPES, null=True, blank=True)
    status = models.CharField(max_length=50, default="active", choices=CAMP_ACTIVITY, null=True, blank=True)
    active = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class Profile(models.Model): #Profile Standard Information
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    picture = models.ImageField(upload_to=random_name_profile_pic, blank=True, null=True)
    full_name = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=50,blank=True,null=True)
    phone_name = models.CharField(max_length=50, null=True, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE,blank=True,null=True)
    hiring_date = models.DateField(blank=True, null=True)
    birth_date = models.DateField(blank=True,null=True)
    role = models.ForeignKey(Role, blank=True, null=True, related_name="profile_role", on_delete=models.CASCADE)

    login_time = models.TimeField(blank=True, null=True)
    #work_status = models.CharField(max_length=50, choices=WORK_CHOICES,default="end_shift")
    email = models.EmailField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', blank=True, null=True)
    dialer_user = models.CharField(max_length=40, blank=True, null=True)
    dialer_password = models.CharField(max_length=40, blank=True, null=True)
    hourly_rate = models.FloatField(null=True, blank=True)
    monthly_salary = models.FloatField(null=True, blank=True)
    salary_type = models.CharField(max_length=20 , choices=SALARY_TYPE, blank=True, null=True)
    phone_number = models.CharField(max_length=50,null=True,blank=True)
    residence = models.CharField(max_length=50, choices=COUNTRIES_CHOICES, null=True, blank=True)
    state = models.CharField(max_length=50, choices=US_STATES_CHOICES, null=True, blank=True)
    joining_date = models.DateField(null=True, blank=True)
    services = models.ManyToManyField(Service, related_name='client_services', blank=True)
    client_status = models.CharField(max_length=50, choices=CAMP_ACTIVITY, default='active',null=True, blank=True)
    discovery_method = models.CharField(max_length=20 , choices=DISCOVERY_TYPE, blank=True, null=True)
    discord = models.CharField(max_length=100, null=True, blank=True)
    payoneer = models.CharField(max_length=100, null=True, blank=True)
    instapay = models.CharField(max_length=100, null=True, blank=True)
    payment_method = models.CharField(max_length=50,default="payoneer", choices=PAYMENT_CHOICES)

    national_id = models.ImageField(upload_to=random_name_national_id, blank=True, null=True)


    settings_theme = models.CharField(max_length=50,default="white", choices=THEME_CHOICES)
    maps_theme = models.CharField(max_length=50,default="white", choices=THEME_CHOICES)

    active = models.BooleanField(default=True)



    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if not self.id:  # Check if the object has an ID (i.e., it's a new object)
            # Get the last ID in the table and increment by 1
            last_agent = Profile.objects.order_by('-id').first()
            if last_agent:
                self.id = last_agent.id + 1
            else:
                self.id = 1000  # Start with ID 1000 if no agents exist yet
        super().save(*args, **kwargs)



class Dialer(models.Model): # Dialers List
    name = models.CharField(max_length=50, null=True, blank=True)
    dialer_type = models.CharField(max_length=50, choices=DIALER_TYPES, null=True, blank=True)
    active = models.BooleanField(default=True)  


class DataSource(models.Model): # List Pull & Skip Tracing Sources

    name = models.CharField(max_length=50, null=True, blank=True)
    source_type = models.CharField(max_length=50, choices=DATASOURCE_TYPES, null=True, blank=True)

    active = models.BooleanField(default=True)



class Campaign(models.Model): # Client Campaigns
    time = models.TimeField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    client = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    agents_count = models.PositiveIntegerField(default=0)
    agents_rate = models.PositiveIntegerField(default=0)
    weekly_hours = models.PositiveIntegerField(default=0)
    datasources = models.ManyToManyField(DataSource, related_name='datasources_campaign', blank=True)

    campaign_type = models.CharField(max_length=50, choices=SERVICE_TYPES, null=True, blank=True)

    lead_points = models.PositiveIntegerField(default=0)
    
    dialer = models.ForeignKey(Dialer, on_delete=models.CASCADE,null=True, blank=True)
    
    


    status = models.CharField(max_length=50, choices=CAMP_ACTIVITY, null=True, blank=True)

    active = models.BooleanField(default=True)

class CampaignCredentials(models.Model):
    campaign = models.OneToOneField(Campaign, on_delete=models.CASCADE, null=True, blank=True)
    dialer = models.ForeignKey(Dialer, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=50, null=True, blank=True)
    password = models.CharField(max_length=50, null=True, blank=True)


class DataSourceCredentials(models.Model):
    campaign = models.OneToOneField(Campaign, on_delete=models.CASCADE, null=True, blank=True)
    datasource = models.ForeignKey(DataSource, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=50, null=True, blank=True)
    password = models.CharField(max_length=50, null=True, blank=True)

class CampaignDispoSetting(models.Model):
    time = models.TimeField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="camp_dispo",null=True, blank=True)

    active = models.BooleanField(default=True)



class ContactList(models.Model): # List Pulled
    start_time = models.TimeField(null=True,blank=True)
    start_date = models.DateField(null=True,blank=True)
    end_time = models.TimeField(null=True,blank=True)
    end_date = models.DateField(null=True,blank=True)   
    id = models.PositiveIntegerField(primary_key=True, editable=True, unique=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="list_campaign",null=True, blank=True)
    contacts = models.IntegerField(null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    county = models.CharField(max_length=50, null=True, blank=True)
    source = models.CharField(max_length=50, null=True, blank=True)
    skip_tracing = models.CharField(max_length=50, null=True, blank=True)
    dialer = models.ForeignKey(Dialer, on_delete=models.CASCADE, blank=True, null=True)

    active = models.BooleanField(default=True)

class DialerListPerformance(models.Model): # Call Dispos
    time = models.TimeField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    dialer_list = models.ForeignKey(ContactList, on_delete=models.CASCADE, related_name="performance_list",null=True, blank=True)
    campaign = models.ForeignKey(ContactList, on_delete=models.CASCADE, related_name="performance_camp",null=True, blank=True)
    dispo = models.ForeignKey(CampaignDispoSetting, on_delete=models.CASCADE, related_name="performance_dispos",null=True, blank=True)
    dispo_count = models.IntegerField(default=0, null=True, blank=True)

    active = models.BooleanField(default=True)



class Lead(models.Model):
    pushed_time = models.TimeField(null=True,blank=True)
    pushed_date = models.DateField(null=True,blank=True)
    lead_id = models.PositiveIntegerField(primary_key=True, editable=True, unique=True)
    agent = models.ForeignKey(User, on_delete=models.CASCADE)
    agent_name = models.CharField(max_length=50, null=True, blank=True)
    agent_user = models.CharField(max_length=50, null=True, blank=True)
    dialer_nick = models.CharField(max_length=50, null=True, blank=True)
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE, related_name="lead_campaign", null=True, blank=True)
    dialer_list = models.ForeignKey(ContactList, on_delete=models.CASCADE, related_name="lead_list", null=True, blank=True)
    property_type = models.CharField(max_length=50, choices=PROPERTY_CHOICES, default="house",null=True, blank=True)
    lead_status = models.CharField(max_length=50, choices=LEAD_CHOICES, default='pending', null=True, blank=True)
    seller_name = models.CharField(max_length=50, null=True, blank=True)
    seller_phone = models.CharField(max_length=50, null=True, blank=True)
    seller_email = models.CharField(max_length=50, null=True, blank=True)
    timeline = models.CharField(max_length=50, choices=TIMELINE_CHOICES, default="two_weeks" ,null=True, blank=True)
    reason = models.TextField(null=True, blank=True)
    property_address = models.TextField( null=True, blank=True)
    asking_price = models.CharField(max_length=50, null=True, blank=True)
    market_value = models.CharField(max_length=50, null=True, blank=True)
    general_info = models.TextField( null=True, blank=True)
    zillow_url = models.TextField(null=True,blank=True)
    callback = models.CharField(max_length=50, null=True, blank=True)
    extra_notes = models.TextField( null=True, blank=True)
    quality_notes = models.TextField( null=True, blank=True)
    quality_to_agent_notes = models.TextField(  null=True, blank=True)
    handled_by = models.ForeignKey(User,on_delete=models.CASCADE, related_name="handled_by_lead_post",null=True,blank=True)
    active = models.BooleanField(default=True)