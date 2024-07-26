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
    context = {"settings":settings,}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile
    return render(request,'admin/admin-home.html',context)


@login_required
def campaigns_table(request):

    context = {"settings":settings,}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile
    context['campaigns'] = Campaign.objects.filter(active=True)
                                                   #add accounts in data sources


    return render(request,'admin/campaigns/campaigns.html',context)




@login_required
def campaign_create(request):


    context = {"settings":settings,}
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
        agent_user = User.objects.create(username=username,password=password)
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
            
    
    return render(request,'admin/agents/agent_create.html',context)





@login_required
def campaign_modify(request,username):

    context = {"settings":settings,}
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
class DeleteCampaignView(View):
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










@login_required
def agents_table(request):

    context = {"settings":settings,}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile
    excluded_roles = []
    excluded_roles.append(Role.objects.get(role_name="Client"))
    context['accounts'] = Profile.objects.filter(active=True).exclude(role__in=excluded_roles)

    return render(request,'admin/agents/agents.html',context)




@login_required
def agent_create(request):


    context = {"settings":settings,}
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
        agent_user = User.objects.create(username=username,password=password)
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
            
    
    return render(request,'admin/agents/agent_create.html',context)





@login_required
def agent_modify(request,username):

    context = {"settings":settings,}
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

    context = {"settings":settings,}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile
    client_role = Role.objects.get(role_name='Client')
    context['accounts'] = Profile.objects.filter(active=True, role=client_role)

    return render(request,'admin/clients/clients.html',context)



@login_required
def client_create(request):


    context = {"settings":settings,}
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
        agents_count = int(data.get('agents_count'))

        services = Service.objects.filter(id__in=selected_services_ids)
        role = Role.objects.get(role_name="Client")
        agent_user = User.objects.create(username=username,password=password)
        

        agent = Profile.objects.create(
            full_name=full_name,
            user=agent_user,
            password=password,
            email=email,
            phone_number=phone,
            state=state,
            role=role,
            joining_date=joining_date,
            discovery_method=discovery_method,
            agents_count=agents_count,
        )
        agent.services.add(*services)
        return redirect('/admin-clients')
            
    
    return render(request,'admin/clients/client_create.html',context)





@login_required
def client_modify(request,username):

    context = {"settings":settings,}
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
            


            agent_profile = Profile.objects.get(user=user)
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




@login_required
def services_table(request):

    context = {"settings":settings,}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile
    context['services'] = Service.objects.filter(active=True)
 
    return render(request,'admin/services/services.html',context)



@login_required
def service_create(request):


    context = {"settings":settings,}
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
            target_service.active=False
            target_service.save()
            return JsonResponse({'message': 'Account deleted successfully.'}, status=200)
        
        else:
            return JsonResponse({'error': 'Invalid password.'}, status=401)




@login_required
def dialers_table(request):

    context = {"settings":settings,}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile
    context['dialers'] = Dialer.objects.filter(active=True)
 
    return render(request,'admin/dialers/dialers.html',context)



@login_required
def dialer_create(request):


    context = {"settings":settings,}
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
            target_service.active=False
            target_service.save()
            return JsonResponse({'message': 'Account deleted successfully.'}, status=200)
        
        else:
            return JsonResponse({'error': 'Invalid password.'}, status=401)





@login_required
def dataSources_table(request):

    context = {"settings":settings,}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile
    context['datasources'] = DataSource.objects.filter(active=True)
 
    return render(request,'admin/datasources/datasources.html',context)



@login_required
def dataSource_create(request):


    context = {"settings":settings,}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile

    context['source_types'] = DATASOURCE_TYPES

    if request.method == "POST":
        data = request.POST
        source_name = data.get('source_name')
        source_type = data.get('source_type')
        

        service = DataSource.objects.create(
            name=source_name,
            source_type=source_type,
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
            target_source.active=False
            target_source.save()
            return JsonResponse({'message': 'Account deleted successfully.'}, status=200)
        
        else:
            return JsonResponse({'error': 'Invalid password.'}, status=401)



