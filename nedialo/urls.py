from django.contrib import admin
from django.urls import path
from core.views import *
from admin.views import *
from operations.views import *
from sales.views import *
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [


    path('admin', applications_table),
    #path('applications', applications_table),
    path('application-form/<int:app_id>', application_report),
    path('crm-admin/', admin.site.urls),
    path('', home),
    path('login', loginview),
    path('logout/',logoutview),
    path('settings',account_settings),
    path('payment_info/', payment_info, name='payment_info'),
    path('update-theme/', update_theme, name='update_theme'),
    path('maps-theme/', maps_theme, name='maps_theme'),
    path('autocomplete/', address_autocomplete, name='address_autocomplete'),
    path('upload-profile/', upload_profile, name='upload_profile'),
    path('upload-id/<int:userid>/', upload_id, name='upload_id'),

    path('admin-campaigns', campaigns_table),
    path('campaign-create', campaign_create),
    path('campaign-modify/<int:camp_id>', campaign_modify),
    path('campaign-delete/<int:camp_id>/', DeleteCampaignView.as_view()),

    path('admin-contactlists', contactlists_table),
    path('contactlist-create', contactlist_create),
    #path('contactlist-modify/<int:contactlist_id>', contactlist_modify),
    path('contactlist-delete/<int:contactlist_id>/', DeleteContactListView.as_view()),



    path('dialercredentials/<int:campaign_id>', dialer_creds_table),
    path('dialercredentials-create/<int:campaign_id>', dialer_cred_create),
    path('dialercredentials-delete/<int:cred_id>/', DeleteDialerCredView.as_view()),


    path('sourcecredentials/<int:campaign_id>', source_creds_table),
    path('sourcecredentials-create/<int:campaign_id>', source_cred_create),
    path('sourcecredentials-delete/<int:cred_id>/', DeleteSourceCredView.as_view()),

    path('admin-agents', agents_table),
    path('agent-create',agent_create),
    path('agent-modify/<str:username>',agent_modify),
    path('agent-delete/<str:username>/', DeleteUserView.as_view()),


    path('admin-clients', clients_table),
    path('client-create',client_create),
    path('client-modify/<str:username>',client_modify),
    path('client-delete/<str:username>/', DeleteClientView.as_view()),


    path('admin-services', services_table),
    path('service-create',service_create),
    path('service-delete/<int:service_id>/', DeleteServiceView.as_view()),

    path('admin-dialers', dialers_table),
    path('dialer-create',dialer_create),
    path('dialer-delete/<int:dialer_id>/', DeleteDialerView.as_view()),


    path('admin-datasources', dataSources_table),
    path('datasource-create',dataSource_create),
    path('datasource-delete/<int:source_id>/', DeleteDataSourceView.as_view()),




    path('lead-submission',lead_submission),
    path('apply', application_form),
    path('application-record/',handle_audio_upload, name='application_record'),



    path('my-leads/<int:month>-<int:year>',my_leads),
    path('lead-report/<int:lead_id>', lead_report),
    path('quality-feedback/<int:month>-<int:year>', leads_quality),
    path('lead-scoring/<int:month>-<int:year>',lead_scoring),
    path('leads-leaderboard/<int:month>-<int:year>',leads_leaderboard),

    path('quality-pending',quality_pending),
    path('lead-reports/<int:month>-<int:year>',quality_lead_reports),
    path('agent-leads/<int:agent_id>-<int:month>-<int:year>',agent_lead_reports),
    path('fireback-lead/<int:lead_id>/', fire_lead, name='fire-lead'),

    path('lead-handling/<int:lead_id>', lead_handling, name='lead_handling'),
    path('get-lead-status/<int:lead_id>/',get_lead_status, name='get_lead_status'),
    path('feedbacks', feedbacks_table),
    path('feedbacks-agent/<int:agent_id>', feedbacks_agent),

    path('feedback-single', feedback_single),
    path('feedback-multiple', feedback_multiple),
    path('feedback-report/<int:id>',feedback_report),

    path('quality-agents/<int:month>-<int:year>',quality_agents),


    path('work-status-data/', work_status_data, name='work_status_data'),

    path('update-status/', update_status, name='update_status'),




    path('leave-requests',leave_request_list),
    path('new-leave',leave_request, name="file_upload"),

    path('delete-leave/<int:leave_id>/', delete_leave, name='delete-leave'),

    path('leave-handling',leave_handling_list),

    path('leave-report/<int:leave_id>',leave_report),


    path('prepayment-requests',prepayment_request_list),
    path('new-prepayment',prepayment_request, name="file_upload"),

    path('delete-prepayment/<int:prepayment_id>/', delete_prepayment, name='delete-prepayment'),

    path('prepayments-handling',prepayment_handling_list),

    path('prepayment-report/<int:prepayment_id>',prepayment_report),





    path('action-requests',action_request_list),
    path('new-action',action_request, name="file_upload"),

    path('delete-action/<int:action_id>/', delete_action, name='delete-action'),

    path('action-handling',action_handling_list),

    path('action-report/<int:action_id>',action_report),


    path('seats', seats),
    path('seat-breakdown/<int:seat_id>-<int:month>-<int:year>', seat_breakdown),
    path('agent-seat-breakdown/<int:agent_id>-<int:month>-<int:year>', agent_seat_breakdown),

    path('update-seat-agent/<int:seat_id>/', update_seat_agent_profile, name='update_seat_agent_profile'),
    path('unseat/<int:agent_id>/', unseat_agent, name='unseat_agent'),
    path('seatlog-delete/<int:log_id>/', DeleteSeatLogView.as_view()),


    path('agents-list-company', agents_list_company),
    path('agents-list-team/<int:team_id>', agents_list_team),

    path('update_status_admin/', update_status_admin, name='update_status_admin'),

    path('camphours-daily/<int:camp_id>-<int:month>-<int:year>', camp_hours_daily),

    path('camphours-monthly/<int:camp_id>-<int:month>-<int:year>', camp_hours_monthly),
    path('camphours-yearly/<int:camp_id>-<int:year>', camp_hours_yearly),

    path('all-campaigns-performance/<int:month>-<int:year>', all_campaigns_performance),

    path('campleads-daily/<int:camp_id>-<int:month>-<int:year>', camp_leads_daily),

    path('campleads-monthly/<int:camp_id>-<int:month>-<int:year>', camp_leads_monthly),
    path('campleads-yearly/<int:camp_id>-<int:year>', camp_leads_yearly),


    path('working-hours-company/<int:month>-<int:year>', working_hours_company),
    path('working-hours-team/<int:team_id>-<int:month>-<int:year>', working_hours_team),
    path('agent-hours/<int:agent_id>-<int:month>-<int:year>', agent_hours),

    path('adjusting-hours', adjusting_hours),
    path('adjusting-hours-form', adjusting_hours_form),

    path('salaries-table-company/<int:month>-<int:year>', salary_company),
    path('salaries-table-team/<int:team_id>-<int:month>-<int:year>', salary_team),
    path('invoice/<int:agent_id>-<int:month>-<int:year>', invoice),


    path('attendance-monitor-company/<int:month>-<int:year>',attendance_company),
    path('attendance-monitor-team/<int:team_id>-<int:month>-<int:year>',attendance_team),
    path('attendance-monitor-agent/<int:agent_id>-<int:month>-<int:year>',attendance_agent),


    path('lateness-monitor-company/<int:month>-<int:year>', lateness_company),
    path('lateness-monitor-team/<int:team_id>-<int:month>-<int:year>',lateness_team),
    path('lateness-monitor-agent/<int:agent_id>-<int:month>-<int:year>',lateness_agent),

    

    path('report-absence',report_absence),


    path('sales-dashboard-<int:year>',sales_dashboard),
    path('sales-lookerstudio',sales_lookerstudio),
    path('sales-calendar-<int:month>-<int:year>', sales_calendar),


    path('sales-lead-submit/', SalesLeadSubmitView.as_view(), name='sales_lead_submit'),

    path('sales-lead-update/', update_sales_lead, name='sales_lead_update'),

    path('sales-lead-update-status/', UpdateLeadStatusView.as_view(), name='update-lead-status'),


    path('sales-lead-data/', sales_leads_data, name='sales_leads_data'),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




