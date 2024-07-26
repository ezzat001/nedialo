from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(ServerSetting)
class ServerSettingAdmin(admin.ModelAdmin):
    list_display = ('company_name',)
    readonly_fields = ('id',)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_name','active')
    readonly_fields = ('id',)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name','id','user','password','role','hourly_rate','phone_number','active')
    filter_horizontal = ('services',)

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name','time','date','position','active')
    readonly_fields = ('id',)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name','active')
    readonly_fields = ('id',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'status','active')


@admin.register(Dialer)
class DialerAdmin(admin.ModelAdmin):
    list_display = ('name', 'dialer_type','active')

@admin.register(DataSource)
class DataSourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'source_type','active')



@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'client','active')
    filter_horizontal = ('datasources',)
