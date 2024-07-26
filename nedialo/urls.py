from django.contrib import admin
from django.urls import path
from core.views import *
from admin.views import *
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [

    path('test/', test_view, name='test_view'),  # 

    path('admin', admin_home),
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
    path('campaign-modify', campaign_modify),
    path('campaign-delete', DeleteCampaignView.as_view()),

    path('admin-agents', agents_table),
    path('agent-create',agent_create),
    path('agent-modify/<str:username>',agent_modify),
    path('agent-delete/<str:username>/', DeleteUserView.as_view()),

    path('admin-clients', clients_table),
    path('client-create',client_create),
    path('client-modify/<str:username>',client_modify),


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


]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




