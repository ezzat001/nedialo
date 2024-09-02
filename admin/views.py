from django.shortcuts import render, redirect
from core.views import settings
from core.models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.core.files.base import ContentFile
from django.utils.decorators import method_decorator
from django.middleware.csrf import CsrfViewMiddleware
from nedialo.constants import countries, us_states, discovery_options
import json

# Create your views here.
@login_required
def admin_home(request):
    context = {}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile
    return render(request,'admin/admin-home.html',context)


@login_required
def campaigns_table(request):

    context = {}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile
    context['campaigns'] = Campaign.objects.filter(active=True)
                                                   #add accounts in data sources


    return render(request,'admin/campaigns/campaigns.html',context)




@login_required
def campaign_create(request):


    context = {}
    profile = Profile.objects.get(user=request.user)

    client_role = Role.objects.get(role_name="Client")

    context['profile'] = profile
    context['clients'] = ClientProfile.objects.filter(role=client_role, active=True)
    context['countries'] = countries
    context['sources'] = DataSource.objects.filter(active=True, data_source=True)
    context['campaign_types'] = SERVICE_TYPES
    context['dialers'] = Dialer.objects.filter(active=True)



    if request.method == "POST":
        data = request.POST
        campaign_name = data.get('campaign_name')
        client = data.get('client')
        agents_count = data.get('agents_count')
        agents_rate = data.get('hourly_rate')
        weekly_hours = data.get('weekly_hours')
        lead_points = data.get('lead_points')
        campaign_type = data.get('campaign_type')
        campaign_dialer = data.get('campaign_dialer')
        selected_sources_ids = data.getlist('campaign_sources')

        sources = DataSource.objects.filter(id__in=selected_sources_ids)

        camp_client = ClientProfile.objects.get(user=User.objects.get(username=client))
        if campaign_dialer == "none":
            camp_dialer = None
        else:
            camp_dialer = Dialer.objects.get(id=campaign_dialer)

        campaign = Campaign.objects.create(
            name = campaign_name,
            client = camp_client,
            agents_count = agents_count,
            agents_rate = agents_rate,
            weekly_hours = weekly_hours,
            lead_points = lead_points,

            campaign_type = campaign_type,
            dialer = camp_dialer,

        )
        campaign.datasources.add(*sources)

        return redirect('/admin-campaigns')

            
    
    return render(request,'admin/campaigns/campaign_create.html',context)





@login_required
def campaign_modify(request,camp_id):

    context = {}


    context['profile'] = Profile.objects.get(user=request.user)
    context['sources'] = DataSource.objects.filter(active=True, data_source=True)
    context['campaign_types'] = SERVICE_TYPES
    context['dialers'] = Dialer.objects.filter(active=True)
    context['camp'] = Campaign.objects.get(active=True, id=camp_id)
    context['camp_status'] = CAMP_ACTIVITY

    leadsettings = LeadHandlingSettings.objects.filter(active=True, activated=True, campaign=context['camp']).first()
    context['leadsettings'] = leadsettings
    context['leadsettingslength'] = leadsettings.count_non_none_slot_names() if leadsettings else 0

    campaigndispos = CampaignDispoSetting.objects.filter(active=True, campaign=context['camp']).first()
    context['campaigndispos'] = campaigndispos
    context['campaigndisposlength'] = campaigndispos.count_non_none_slot_names() if campaigndispos else 0


    if request.method == "POST":

        if 'general_campaign_settings' in request.POST :
            data = request.POST
            camp_name = data.get('campaign_name')
            agents_count = data.get('agents_count')
            hourly_rate = data.get('hourly_rate')
            weekly_hours = data.get('weekly_hours')
            lead_points = data.get('lead_points')
            campaign_type = data.get('campaign_type')
            campaign_dialer = data.get('dialer')
            camp_status = data.get('campaign_status')

            selected_sources_ids = data.getlist('sources')

            campaign_sources = DataSource.objects.filter(id__in=selected_sources_ids)

            camp = Campaign.objects.get(id=camp_id)

            camp.name = camp_name
            camp.agents_count = agents_count
            camp.agents_rate = hourly_rate
            camp.weekly_hours = weekly_hours
            camp.lead_points = lead_points
            camp.campaign_type = campaign_type
            camp.dialer = Dialer.objects.get(id=campaign_dialer)
            camp.status = camp_status 
            if not selected_sources_ids:
                camp.datasources.clear()  
            else:
                
                camp.datasources.set(campaign_sources)
            camp.save()

            return redirect(request.get_full_path())
        
        if "lead_handling" in request.POST:
            
            campaign = Campaign.objects.get(active=True, id=camp_id)
            data = request.POST

            slot1_name = data.get('slot1_name')
            slot1_percentage = data.get('slot1_percentage')
            slot2_name = data.get('slot2_name')
            slot2_percentage = data.get('slot2_percentage')
            slot3_name = data.get('slot3_name')
            slot3_percentage = data.get('slot3_percentage')
            slot4_name = data.get('slot4_name')
            slot4_percentage = data.get('slot4_percentage')
            slot5_name = data.get('slot5_name')
            slot5_percentage = data.get('slot5_percentage')
            slot6_name = data.get('slot6_name')
            slot6_percentage = data.get('slot6_percentage')
            slot7_name = data.get('slot7_name')
            slot7_percentage = data.get('slot7_percentage')
            slot8_name = data.get('slot8_name')
            slot8_percentage = data.get('slot8_percentage')
            slot9_name = data.get('slot9_name')
            slot9_percentage = data.get('slot9_percentage')
            slot10_name = data.get('slot10_name')
            slot10_percentage = data.get('slot10_percentage')
            
            lead_handling_settings, created = LeadHandlingSettings.objects.update_or_create(
            campaign=campaign,
            defaults={
                'slot1_name': slot1_name if slot1_name not in ["None", None, ""] else None,
                'slot1_percentage': float(slot1_percentage) if slot1_percentage not in ["None", None, ""] else 0.0,
                'slot2_name': slot2_name if slot2_name not in ["None", None, ""] else None,
                'slot2_percentage': float(slot2_percentage) if slot2_percentage not in ["None", None, ""] else 0.0,
                'slot3_name': slot3_name if slot3_name not in ["None", None, ""] else None,
                'slot3_percentage': float(slot3_percentage) if slot3_percentage not in ["None", None, ""] else 0.0,
                'slot4_name': slot4_name if slot4_name not in ["None", None, ""] else None,
                'slot4_percentage': float(slot4_percentage) if slot4_percentage not in ["None", None, ""] else 0.0,
                'slot5_name': slot5_name if slot5_name not in ["None", None, ""] else None,
                'slot5_percentage': float(slot5_percentage) if slot5_percentage not in ["None", None, ""] else 0.0,
                'slot6_name': slot6_name if slot6_name not in ["None", None, ""] else None,
                'slot6_percentage': float(slot6_percentage) if slot6_percentage not in ["None", None, ""] else 0.0,
                'slot7_name': slot7_name if slot7_name not in ["None", None, ""] else None,
                'slot7_percentage': float(slot7_percentage) if slot7_percentage not in ["None", None, ""] else 0.0,
                'slot8_name': slot8_name if slot8_name not in ["None", None, ""] else None,
                'slot8_percentage': float(slot8_percentage) if slot8_percentage not in ["None", None, ""] else 0.0,
                'slot9_name': slot9_name if slot9_name not in ["None", None, ""] else None,
                'slot9_percentage': float(slot9_percentage) if slot9_percentage not in ["None", None, ""] else 0.0,
                'slot10_name': slot10_name if slot10_name not in ["None", None, ""] else None,
                'slot10_percentage': float(slot10_percentage) if slot10_percentage not in ["None", None, ""] else 0.0,
                'activated': True,
                }
            )

            return redirect(request.get_full_path())
        
        if "camp_dispos" in request.POST:
            campaign = Campaign.objects.get(active=True, id=camp_id)
            data = request.POST

            dispo_data = {f"slot{i}_dispo": data.get(f"slot{i}_dispo") for i in range(1, 16)}

            defaults = {
                f'slot{i}_dispo': dispo_data[f"slot{i}_dispo"] if dispo_data[f"slot{i}_dispo"] not in ["None", None, ""] else None
                for i in range(1, 16)
            }
            defaults['active'] = True 

            campaign_dispo_setting, created = CampaignDispoSetting.objects.update_or_create(
                campaign=campaign,
                defaults=defaults
            )
            return redirect(request.get_full_path())


            

    return render(request,'admin/campaigns/campaign_modify.html',context)


@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_protect, name='dispatch')
@method_decorator(require_http_methods(["POST"]), name='dispatch')
class DeleteCampaignView(View):
    def post(self, request, camp_id):
        current_user = request.user

        # Ensure correct data access
        try:
            body = json.loads(request.body)
            password = body['password']
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Password not provided.'}, status=400)

        # Authenticate user based on current_user and provided password
        user = authenticate(username=current_user.username, password=password)

        if user is not None:
            # Check if the authenticated user can delete the target user
            target_camp = get_object_or_404(Campaign, id=camp_id)
            target_camp.delete()
            return JsonResponse({'message': 'Account deleted successfully.'}, status=200)
        
        else:
            return JsonResponse({'error': 'Invalid password.'}, status=401)




@login_required
def contactlists_table(request):

    context = {}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile
    context['contactlists'] = ContactList.objects.filter(active=True)


    return render(request,'admin/campaigns/contactlists.html',context)




@login_required
def contactlist_create(request):


    context = {}
    profile = Profile.objects.get(user=request.user)

    client_role = Role.objects.get(role_name="Client")

    context['profile'] = profile
    context['campaigns'] = Campaign.objects.filter(active=True)

    context['sources'] = DataSource.objects.filter(active=True, source_type__in=["pulling","skip_pull"])
    context['skiptracing'] = DataSource.objects.filter(active=True, source_type__in=['skip_tracing','skip_pull',])
    context['campaign_types'] = SERVICE_TYPES
    context['states'] = US_STATES_CHOICES
    context['statuses'] = LIST_STATUS_CHOICES



    if request.method == "POST":
        data = request.POST
        list_name = data.get('list_name')
        campaign = int(data.get('camp'))
        contacts = int(data.get('contacts'))
        status = data.get('status')
        source = int(data.get('source'))
        skip_tracing = int(data.get('skiptracing'))
        states = data.getlist('states')
        
        source = DataSource.objects.get(id=source)
        skip_tracing = DataSource.objects.get(id=skip_tracing)

        campaign = Campaign.objects.get(id=campaign)
        dialer = campaign.dialer
        contactlist = ContactList.objects.create(
            name = list_name,
            campaign = campaign,
            contacts = contacts,
            dialer = dialer,
            source = source,
            skip_tracing = skip_tracing,
            states = states,
            status = status,
        )

        return redirect('/admin-contactlists')

            
    
    return render(request,'admin/campaigns/contactlist_create.html',context)






@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_protect, name='dispatch')
@method_decorator(require_http_methods(["POST"]), name='dispatch')
class DeleteContactListView(View):
    def post(self, request, contactlist_id):
        current_user = request.user

        # Ensure correct data access
        try:
            body = json.loads(request.body)
            password = body['password']
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Password not provided.'}, status=400)

        # Authenticate user based on current_user and provided password
        user = authenticate(username=current_user.username, password=password)

        if user is not None:
            # Check if the authenticated user can delete the target user
            target_list = get_object_or_404(ContactList, id=contactlist_id)
            target_list.delete()
            return JsonResponse({'message': 'Account deleted successfully.'}, status=200)
        
        else:
            return JsonResponse({'error': 'Invalid password.'}, status=401)




@login_required
def dialer_creds_table(request,campaign_id):

    context = {}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile
    campaign = Campaign.objects.get(id=campaign_id)
    context['campaign'] = campaign
    context['dialer_creds'] = DialerCredentials.objects.filter(campaign=campaign,active=True)


    return render(request,'admin/credentials/dialer_creds.html',context)




@login_required
def dialer_cred_create(request,campaign_id):


    context = {}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile
    campaign = Campaign.objects.get(id=campaign_id)
    context['campaign'] = campaign
    context['account_types'] = DIALER_ACCOUNT_TYPE



    if request.method == "POST":
        data = request.POST
        username = data.get('username')
        password = data.get('password')
        account_type = data.get('account_type')

        campaign = Campaign.objects.get(id=campaign_id)
        
        dialer_cred = DialerCredentials.objects.create(
            campaign=campaign,
            dialer=campaign.dialer,
            username=username,
            password=password,
            account_type=account_type,
        )

        return redirect('/dialercredentials/'+str(campaign_id))

            
    
    return render(request,'admin/credentials/dialer_cred_create.html',context)








@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_protect, name='dispatch')
@method_decorator(require_http_methods(["POST"]), name='dispatch')
class DeleteDialerCredView(View):
    def post(self, request, cred_id):
        current_user = request.user

        # Ensure correct data access
        try:
            body = json.loads(request.body)
            password = body['password']
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Password not provided.'}, status=400)

        # Authenticate user based on current_user and provided password
        user = authenticate(username=current_user.username, password=password)

        if user is not None:
            # Check if the authenticated user can delete the target user
            target_cred = get_object_or_404(DialerCredentials, id=cred_id)
            
            target_cred.delete()
            return JsonResponse({'message': 'Account deleted successfully.'}, status=200)
        
        else:
            return JsonResponse({'error': 'Invalid password.'}, status=401)







@login_required
def source_creds_table(request,campaign_id):

    context = {}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile
    campaign = Campaign.objects.get(id=campaign_id)
    context['campaign'] = campaign
    context['source_creds'] = DataSourceCredentials.objects.filter(campaign=campaign,active=True)


    return render(request,'admin/credentials/source_creds.html',context)




@login_required
def source_cred_create(request,campaign_id):


    context = {}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile
    campaign = Campaign.objects.get(id=campaign_id)
    context['campaign'] = campaign
    context['sources'] = DataSource.objects.filter(active=True)
    context['account_types'] = SOURCE_ACCOUNT_TYPE



    if request.method == "POST":
        data = request.POST
        source_id = data.get('source')
        username = data.get('username')
        password = data.get('password')
        account_type = data.get('account_type')

        campaign = Campaign.objects.get(id=campaign_id)
        source = DataSource.objects.get(id=source_id)
        source_cred = DataSourceCredentials.objects.create(
            campaign=campaign,
            datasource=source,
            username=username,
            password=password,
            account_type=account_type,
        )

        return redirect('/sourcecredentials/'+str(campaign_id))

            
    
    return render(request,'admin/credentials/source_cred_create.html',context)








@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_protect, name='dispatch')
@method_decorator(require_http_methods(["POST"]), name='dispatch')
class DeleteSourceCredView(View):
    def post(self, request, cred_id):
        current_user = request.user

        # Ensure correct data access
        try:
            body = json.loads(request.body)
            password = body['password']
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Password not provided.'}, status=400)

        # Authenticate user based on current_user and provided password
        user = authenticate(username=current_user.username, password=password)

        if user is not None:
            # Check if the authenticated user can delete the target user
            target_cred = get_object_or_404(DataSourceCredentials, id=cred_id)
            
            target_cred.delete()
            return JsonResponse({'message': 'Account deleted successfully.'}, status=200)
        
        else:
            return JsonResponse({'error': 'Invalid password.'}, status=401)









@login_required
def agents_table(request):

    context = {}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile
    excluded_roles = []
    excluded_roles.append(Role.objects.get(role_name="Client"))
    context['accounts'] = Profile.objects.filter(active=True).exclude(role__in=excluded_roles)

    return render(request,'admin/agents/agents.html',context)




@login_required
def agent_create(request):


    context = {}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile
    context['roles'] = Role.objects.filter(active=True)
    context['teams'] = Team.objects.filter(active=True)
    context['countries'] = countries



    if request.method == "POST":
        data = request.POST
        full_name = data.get('full_name')
        username = data.get('username')
        password = data.get('password')
        phone_name = data.get('phone_name')
        phone = data.get('phone')
        discord = data.get('discord')
        residence = data.get('residence')
        birth_date = data.get('birth_date')
        role = data.get('role')
        team = data.get('team')
        login_time = data.get('login_time')
        hiring_date = data.get('hiring_date')
        hourly_rate = data.get('hourly_rate')
        monthly_salary = data.get('monthly_salary')
        salary_type = data.get('salary_type')
        national_id = request.FILES.get('national_id')  # Get the uploaded file
        role = Role.objects.get(id=int(role), active=True)
        team = Team.objects.get(id=int(team), active=True)            
        agent_user = User.objects.create(username=username)
        agent_user.set_password(password)
        agent_user.save()
        agent = Profile.objects.create(
            full_name=full_name,
            user=agent_user,
            password=password,
            phone_name=phone_name,
            phone_number=phone,
            discord=discord,
            residence=residence,
            birth_date=birth_date,
            role=role,
            team=team,
            login_time=login_time,
            hiring_date=hiring_date,
            hourly_rate=hourly_rate,
            monthly_salary=monthly_salary,
            salary_type=salary_type,
            national_id=national_id  # Save the file to the model
        )

        return redirect('/admin-agents')
            
    
    return render(request,'admin/agents/agent_create.html',context)





@login_required
def agent_modify(request,username):

    context = {}
    user = User.objects.get(username=username)

    context['agent_profile'] = Profile.objects.get(user=user)

    context['profile'] = Profile.objects.get(user=request.user)
    context['roles'] = Role.objects.filter(active=True)
    context['teams'] = Team.objects.filter(active=True)
    context['countries'] = countries
    unavailable_roles = ['Client', 'Affiliate']
    if context['agent_profile'].role.role_name in unavailable_roles:
        return redirect('/admin')

    if request.method == "POST":

        if 'payment_method' in request.POST :
            data = request.POST
            payoneer_account = data.get('payoneer_account')
            instapay_account = data.get('instapay_account')
            salary_type = data.get('salary_type')
            salary_account = data.get('salary_account')
            hourly_rate = data.get('hourly_rate')
            monthly_salary = data.get('monthly_salary')

            agent_profile = Profile.objects.get(user=user)
            
            agent_profile.payoneer = payoneer_account
            agent_profile.instapay = instapay_account
            agent_profile.salary_type = salary_type
            agent_profile.payment_method = salary_account
            if salary_type == "hourly":
                agent_profile.hourly_rate = float(hourly_rate)
            elif salary_type == "monthly":
                agent_profile.monthly_salary = float(monthly_salary)
            else:
                pass
            agent_profile.save()
            return redirect(request.get_full_path())
        if 'account_info' in request.POST :
            data = request.POST
            full_name = data.get('full_name')
            email = data.get('email')
            phone_number = data.get('phone_number')
            discord = data.get('discord')
            birth_date = data.get('birth_date')
            hiring_date = data.get('hiring_date')
            login_time = data.get('login_time')
            team = data.get('team')
            role = data.get('role')
            residence = data.get('residence')
            
            team_obj = Team.objects.get(id=int(team))
            role_obj = Role.objects.get(id=int(role))

            agent_profile = Profile.objects.get(user=user)
            agent_profile.full_name = full_name
            agent_profile.email = email
            agent_profile.phone_number = phone_number
            agent_profile.discord = discord
            agent_profile.birth_date = birth_date
            agent_profile.hiring_date = hiring_date
            agent_profile.login_time = login_time
            agent_profile.team = team_obj
            agent_profile.role = role_obj
            agent_profile.residence = residence

            agent_profile.save()

            return redirect(request.get_full_path())

        



    
    return render(request,'admin/agents/agent_modify.html',context)




@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_protect, name='dispatch')
@method_decorator(require_http_methods(["POST"]), name='dispatch')
class DeleteUserView(View):
    def post(self, request, username):
        current_user = request.user

        # Ensure correct data access
        try:
            body = json.loads(request.body)
            password = body['password']
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Password not provided.'}, status=400)

        # Authenticate user based on current_user and provided password
        user = authenticate(username=current_user.username, password=password)

        if user is not None:
            # Check if the authenticated user can delete the target user
            target_user = get_object_or_404(User, username=username)
            target_profile = get_object_or_404(Profile, user=target_user)
            target_profile.active=False
            target_profile.save()
            return JsonResponse({'message': 'Account deleted successfully.'}, status=200)
        
        else:
            return JsonResponse({'error': 'Invalid password.'}, status=401)



def upload_id(request, userid):
    if request.method == 'POST':
        if 'national_id' in request.FILES:  # Match with the name attribute in the form
            file = request.FILES['national_id']  # Use the same key as the file input
            # Check if the uploaded file is an image
            if file.content_type.startswith('image'):
                # Example: Save the file to a Profile model instance
                profile = get_object_or_404(Profile, id=userid)
                profile.national_id = file
                profile.save()
                return redirect('/agent-modify/'+str(profile.user))
            else:
                return JsonResponse({'error': 'File is not an image.'}, status=400)
        else:
            return JsonResponse({'error': 'File not provided.'}, status=400)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)



@login_required
def clients_table(request):

    context = {}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile
    client_role = Role.objects.get(role_name='Client')
    context['accounts'] = ClientProfile.objects.filter(active=True, role=client_role)

    return render(request,'admin/clients/clients.html',context)



@login_required
def client_create(request):


    context = {}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile

    context['us_states'] = us_states
    context['services'] = Service.objects.filter(active=True, status="active")
    context['discovery_options'] = discovery_options


    if request.method == "POST":
        data = request.POST
        full_name = data.get('full_name')
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        phone = data.get('phone')
        state = data.get('residence')
        joining_date = data.get('joining_date')
        selected_services_ids = data.getlist('services')
        discovery_method = data.get('discovery_method')

        services = Service.objects.filter(id__in=selected_services_ids)
        role = Role.objects.get(role_name="Client")
        agent_user = User.objects.create(username=username,password=password)
        

        agent = ClientProfile.objects.create(
            full_name=full_name,
            user=agent_user,
            password=password,
            email=email,
            phone_number=phone,
            state=state,
            role=role,
            joining_date=joining_date,
            discovery_method=discovery_method,
        )
        agent.services.add(*services)
        return redirect('/admin-clients')
            
    
    return render(request,'admin/clients/client_create.html',context)





@login_required
def client_modify(request,username):

    context = {}
    user = User.objects.get(username=username)

    context['agent_profile'] = Profile.objects.get(user=user)
    context['profile'] = Profile.objects.get(user=request.user)
    context['us_states'] = us_states
    context['discovery_options'] = discovery_options
    context['services'] = Service.objects.filter(active=True, status="active")

    if context['agent_profile'].role.role_name != "Client":
        return redirect('/admin')

    if request.method == "POST":

        if 'account_info' in request.POST :
            data = request.POST
            full_name = data.get('full_name')
            email = data.get('email')
            phone_number = data.get('phone_number')
            joining_date = data.get('joining_date')
            discovery_method = data.get('discovery_method')
            selected_services_ids = data.getlist('services')
            state = data.get('residence')
            
            services = Service.objects.filter(id__in=selected_services_ids)
            


            agent_profile = ClientProfile.objects.get(user=user)
            agent_profile.full_name = full_name
            agent_profile.email = email
            agent_profile.phone_number = phone_number
            agent_profile.joining_date = joining_date
            agent_profile.state = state
            agent_profile.discovery_method = discovery_method
            if not selected_services_ids:
                agent_profile.services.clear()  
            else:
                
                agent_profile.services.set(services)
            agent_profile.save()

            return redirect(request.get_full_path())
    return render(request,'admin/clients/client_modify.html',context)


@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_protect, name='dispatch')
@method_decorator(require_http_methods(["POST"]), name='dispatch')
class DeleteClientView(View):
    def post(self, request, username):
        current_user = request.user

        # Ensure correct data access
        try:
            body = json.loads(request.body)
            password = body['password']
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Password not provided.'}, status=400)

        # Authenticate user based on current_user and provided password
        user = authenticate(username=current_user.username, password=password)

        if user is not None:
            # Check if the authenticated user can delete the target user
            target_user = get_object_or_404(User, username=username)
            target_profile = get_object_or_404(ClientProfile, user=target_user)
            target_profile.active=False
            target_profile.save()
            return JsonResponse({'message': 'Account deleted successfully.'}, status=200)
        
        else:
            return JsonResponse({'error': 'Invalid password.'}, status=401)

@login_required
def services_table(request):

    context = {}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile
    context['services'] = Service.objects.filter(active=True)
 
    return render(request,'admin/services/services.html',context)



@login_required
def service_create(request):


    context = {}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile

    context['us_states'] = us_states
    context['services'] = SERVICE_TYPES

    if request.method == "POST":
        data = request.POST
        service_name = data.get('service_name')
        service_type = data.get('service_type')
        

        service = Service.objects.create(
            name=service_name,
            service_type=service_type,
        )

        return redirect('/admin-services')
            
    
    return render(request,'admin/services/service_create.html',context)



@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_protect, name='dispatch')
@method_decorator(require_http_methods(["POST"]), name='dispatch')
class DeleteServiceView(View):
    def post(self, request, service_id):
        current_user = request.user

        # Ensure correct data access
        try:
            body = json.loads(request.body)
            password = body['password']
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Password not provided.'}, status=400)

        # Authenticate user based on current_user and provided password
        user = authenticate(username=current_user.username, password=password)

        if user is not None:
            # Check if the authenticated user can delete the target user
            target_service = get_object_or_404(Service, id=service_id)
            target_service.delete()
            return JsonResponse({'message': 'Account deleted successfully.'}, status=200)
        
        else:
            return JsonResponse({'error': 'Invalid password.'}, status=401)




@login_required
def dialers_table(request):

    context = {}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile
    context['dialers'] = Dialer.objects.filter(active=True)
 
    return render(request,'admin/dialers/dialers.html',context)



@login_required
def dialer_create(request):


    context = {}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile

    context['dialer_types'] = DIALER_TYPES

    if request.method == "POST":
        data = request.POST
        dialer_name = data.get('dialer_name')
        dialer_type = data.get('dialer_type')
        

        service = Dialer.objects.create(
            name=dialer_name,
            dialer_type=dialer_type,
        )

        return redirect('/admin-dialers')
            
    
    return render(request,'admin/dialers/dialer_create.html',context)



@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_protect, name='dispatch')
@method_decorator(require_http_methods(["POST"]), name='dispatch')
class DeleteDialerView(View):
    def post(self, request, dialer_id):
        current_user = request.user

        # Ensure correct data access
        try:
            body = json.loads(request.body)
            password = body['password']
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Password not provided.'}, status=400)

        # Authenticate user based on current_user and provided password
        user = authenticate(username=current_user.username, password=password)

        if user is not None:
            # Check if the authenticated user can delete the target user
            target_service = get_object_or_404(Dialer, id=dialer_id)
            target_service.delete()
            return JsonResponse({'message': 'Account deleted successfully.'}, status=200)
        
        else:
            return JsonResponse({'error': 'Invalid password.'}, status=401)





@login_required
def dataSources_table(request):

    context = {}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile
    context['datasources'] = DataSource.objects.filter(active=True)
 
    return render(request,'admin/datasources/datasources.html',context)



@login_required
def dataSource_create(request):


    context = {}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile

    context['source_types'] = DATASOURCE_TYPES

    if request.method == "POST":
        data = request.POST
        source_name = data.get('source_name')
        source_type = data.get('source_type')
        
        if source_type == "crm" or source_type == "data_management":
            data_source = False
        else:
            data_source = True

        service = DataSource.objects.create(
            name=source_name,
            source_type=source_type,
            data_source=data_source,
        )

        return redirect('/admin-datasources')
            
    
    return render(request,'admin/datasources/datasource_create.html',context)



@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_protect, name='dispatch')
@method_decorator(require_http_methods(["POST"]), name='dispatch')
class DeleteDataSourceView(View):
    def post(self, request, source_id):
        current_user = request.user
        # Ensure correct data access
        try:
            body = json.loads(request.body)
            password = body['password']
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Password not provided.'}, status=400)

        # Authenticate user based on current_user and provided password
        user = authenticate(username=current_user.username, password=password)

        if user is not None:
            # Check if the authenticated user can delete the target user
            target_source = get_object_or_404(DataSource, id=source_id)
            target_source.delete()
            return JsonResponse({'message': 'Account deleted successfully.'}, status=200)
        
        else:
            return JsonResponse({'error': 'Invalid password.'}, status=401)



