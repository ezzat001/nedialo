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

@admin.register(ClientProfile)
class ClientProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name','id','user','password','role','active')
    filter_horizontal = ('services',)
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name','id','user','password','role','hourly_rate','phone_number','active')

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name','submission_date','position','active')
    readonly_fields = ('id','app_uuid')     


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name','team_type','active')
    readonly_fields = ('id',)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_type','active')


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


@admin.register(DialerCredentials)
class DialerCredentialsAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'agent_profile','account_type',"username",'password','active')
    

@admin.register(DataSourceCredentials)
class DataSourceCredentialsAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'datasource','account_type',"username",'password','active')

@admin.register(LeadHandlingSettings)
class LeadHandlingSettingsAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'activated', 'active')

@admin.register(CampaignDispoSetting)
class CampaignDispoSettingAdmin(admin.ModelAdmin):
    list_display = ('campaign', 'active')

@admin.register(ContactList)
class ContactListAdmin(admin.ModelAdmin):
    list_display = ('name','campaign', 'active')

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('agent_user', 'lead_id','campaign','pushed','seller_name','status','handled_by')

 


@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('agent_profile', 'leave_type', 'active')


@admin.register(Action)
class ActionAdmin(admin.ModelAdmin):
    list_display = ('agent', 'action_type', 'active')

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('agent_profile', 'auditor_profile','type', 'feedback_type', 'status')



@admin.register(ManualHours)
class ManualHoursAdmin(admin.ModelAdmin):
    list_display = ('agent_profile','created', 'positive','hours', 'active')


admin.site.register(WorkStatus)


admin.site.register(Absence)

admin.site.register(SeatAssignmentLog)

admin.site.register(Prepayment)


admin.site.register(SalesLead)

admin.site.register(AffiliateInvoice)
admin.site.register(AffiliateProfile)
admin.site.register(Task)

admin.site.register(ContractSample)

admin.site.register(Contract)
admin.site.register(Package)

admin.site.register(ContractVisit)
