from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Application
from django.conf import settings as django_settings
from django.http import JsonResponse,HttpResponse, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django.core import serializers
from django.contrib.sessions.models import Session
from django.template.loader import render_to_string
from django.core.exceptions import ValidationError
from django.db.models import Avg, Count, Q, Sum
from collections import defaultdict


from django.apps import apps
from .models import *
from datetime import datetime,timedelta
import json
from django.utils import timezone as tz
from django.template.defaultfilters import date as _date

from dateutil.relativedelta import relativedelta
from itertools import chain
from operator import attrgetter
import calendar,time
from django.utils.timezone import now
import asyncio
from django.utils.safestring import mark_safe
from django.core.files.storage import default_storage
import os
import requests
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods




try:
    settings = ServerSetting.objects.first()
except:
    settings = None

def format_timedelta(td):
    if td is None:
        return '00:00:00'
    
    # Get total seconds from timedelta
    total_seconds = int(td.total_seconds())
    
    # Calculate hours, minutes, and seconds
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    # Format as HH:MM:SS
    formatted_time = f"{hours:02}:{minutes:02}:{seconds:02}"
    return formatted_time

def format_percentage(number):
    # Format the number to two decimal places and multiply by 100 for percentage
    formatted = f"{number * 100:.2f}"
    # Remove trailing zeros and decimal point if needed
    return formatted.rstrip('0').rstrip('.')


def loginview(request):
    context = {}
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        if str(profile.role) == "client":
            return redirect('/client-dashboard')
        else:
            return redirect('/')
    else:
        if request.method == "POST":
            data = request.POST
            username=data.get('username')
            password = data.get('password')
            
            
            usera = authenticate(username=username,password=password)
            if not usera:
                context['error'] = "Wrong Username or Password"
                return render(request, "login.html", context)            

            userprofile = Profile.objects.get(user=usera)
            active = userprofile.active
            
            active_statuses = ["active","upl","annual","casual","sick"]
            inactive_statuses = ["inactive","dropped","blacklisted"]
            if not active or userprofile.status in inactive_statuses:
                errormessage = "Your Account has been suspended Please Contact Nedialo Admin."
                return render(request, "errors/error-403.html", context={"error_message":errormessage,})            
            if active and userprofile.status in active_statuses:
                    
                login(request,usera)
                return redirect('/')
                
    
    return render(request,'login.html',context)

@login_required
def logoutview(request):

    logout(request)

    return redirect('/login')

@login_required
def home(request):
    today = (tz.localtime(tz.now())).date()
    user = request.user
    try:
        work_status = WorkStatus.objects.get(user=user, date=today)
    except:
        work_status = None
    context = {"settings":settings,
               "work_status":work_status,
               }
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile

    now = tz.now()
    current_year = now.year
    current_month = now.month
    month_name = now.strftime('%B')
    context['month_name'] = month_name
    context['current_year'] = current_year
    monthly_qualified_count = []

    leads = Lead.objects.filter(agent_profile=profile,
                    pushed__year=current_year,
                    pushed__month=current_month)
    

    context['leads_count'] = leads.count()
    total_lead_flow = leads.aggregate(total_lead_flow=Sum('lead_flow'))['total_lead_flow']
    try:
        leads_flow_quality = round((total_lead_flow / leads.count()),2)
    except:
        leads_flow_quality = 0
    context['leads_flow'] = leads_flow_quality


    for month in range(1, 13):
        # Filter leads for the current month and year
        leads_count = Lead.objects.filter(
            agent_profile=profile,
            pushed__year=current_year,
            pushed__month=month,
            status="qualified",
        ).count()
        monthly_qualified_count.append(leads_count)

    monthly_disqualified_count = []

    for month in range(1, 13):
        # Filter leads for the current month and year
        leads_count = Lead.objects.filter(
            agent_profile=profile,
            pushed__year=current_year,
            pushed__month=month,
            status="disqualified",
        ).count()
        monthly_disqualified_count.append(leads_count)
    context['qualified_count'] = monthly_qualified_count
    context['disqualified_count'] = monthly_disqualified_count

    leads = Lead.objects.filter(agent_profile=profile,
                    pushed__year=current_year,
                    pushed__month=current_month,
                    status="qualified")

    leads_per_campaign = leads.values('campaign').annotate(lead_count=Count('lead_id')).order_by('campaign')

# Create a dictionary with campaign objects as keys and lead counts as values
    campaign_leads_count = {
        Campaign.objects.get(pk=item['campaign']).lead_points: item['lead_count']
        for item in leads_per_campaign
    }


    total_points = sum(key * value for key, value in campaign_leads_count.items())

    context['lead_points'] = total_points
    
    monthly_target = settings.monthly_leadpoints_target
    if monthly_target == 0:
        context['target_percentage'] = 0
    else:
        context['target_percentage'] = round((total_points / monthly_target) * 100, 2)


    qualified_count = Lead.objects.filter(
        agent_profile=profile,
        pushed__year=current_year,
        status="qualified",
    ).count()

    disqualified_count = Lead.objects.filter(
        agent_profile=profile,
        pushed__year=current_year,
        status="disqualified",
    ).count()

    callback_count = Lead.objects.filter(
        agent_profile=profile,
        pushed__year=current_year,

        status="callback",
    ).count()

    duplicated_count = Lead.objects.filter(
        agent_profile=profile,
        pushed__year=current_year,

        status="duplicated",
    ).count()
    context['lead_results_year'] = [qualified_count,
            disqualified_count,
            callback_count,
            duplicated_count
        ]


    
    return render(request,'dashboard/agent.html',context)

@login_required
def user_profile(request):
    context = {}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile

    return render(request,'profile.html', context)

@login_required
def lead_submission(request):
    context = {"settings":settings,"api_token":django_settings.HERE_API}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile
    context['campaigns'] = Campaign.objects.filter(status="active")
    context['contactlists'] = ContactList.objects.filter(active=True)
    if request.method == "POST":
        lat,long = 0,0
        data = request.POST
        campid = data.get('campaign')
        contactlistid = data.get('dialer_list')
        prospect_name = data.get('owner_name')
        phone_number = data.get('phone_number')
        email = data.get('email')
        property_type = data.get('property_type')
        address = data.get('address')
        asking_price = data.get('asking_price')
        market_value = data.get('market_value')
        reason = data.get('reason')
        timeline = data.get('timeline')
        zillow_url = data.get('zillow_url')
        callback_time = data.get('callback_time')
        general_info = data.get('general_info')
        extra_info = data.get('extra_info')
        lat,long = data.get('latitude'),data.get('longitude')
        state,county = data.get('state'), data.get('county')
        
    
        agent_profile = Profile.objects.get(user=request.user)
        campaign = Campaign.objects.get(id=campid)
        contact_list = ContactList.objects.get(id=contactlistid)
        lead = Lead.objects.create(
            agent_user=request.user,
            agent_profile=agent_profile,
            campaign=campaign,
            contact_list=contact_list,
            property_type=property_type,
            seller_name = prospect_name,
            seller_phone= phone_number,
            seller_email= email,
            timeline=timeline,
            reason=reason,
            property_address=address,
            asking_price=asking_price,
            market_value=market_value,
            general_info=general_info,
            property_url=zillow_url,
            callback=callback_time,
            extra_notes=extra_info,
            latitude=lat,
            longitude=long,
            state=state,
            county=county,
        )
        return redirect('/')


    return render(request,'leads/lead_submission.html', context)



def my_leads(request):

    now = tz.now()
    current_year = now.year
    current_month = now.month
    current_month_name = _date(now, "F")
    context = {}
    context['month_name'] =current_month_name
    context['year'] = current_year
    context['profile'] = Profile.objects.get(user=request.user)

    context['pending_leads'] = Lead.objects.filter(agent_user=request.user,status="pending", active=True).order_by('-pushed')[:5]

    context['qualified'] = Lead.objects.filter(
        pushed__month=current_month,
        pushed__year=current_year,
        agent_user=request.user,
        status="qualified",
        active=True
        ).count()

    context['disqualified'] = Lead.objects.filter(
        pushed__month=current_month,
        pushed__year=current_year,
        agent_user=request.user,
        status__in = ["disqualified", "duplicate"],
        active=True
        ).count()

    pending_leads = Lead.objects.filter(
        pushed__month=current_month,
        pushed__year=current_year,
        agent_user=request.user,
        status="pending",
        active=True
        )
    
    context['pending'] = pending_leads.count()

    context['callback'] = Lead.objects.filter(
        pushed__month=current_month,
        pushed__year=current_year,
        agent_user=request.user,
        status="callback",
        active=True
        ).count()
    

    context['total'] =  Lead.objects.filter(
        pushed__month=current_month,
        pushed__year=current_year,
        agent_user=request.user,
        active=True
        ).count()
    

    context['leads_list'] =  Lead.objects.filter(
        pushed__month=current_month,
        pushed__year=current_year,
        agent_user=request.user,
        active=True
        ).order_by("-pushed")[:6]
    
   
    

    def calculate_percentage(part, whole):
        if whole == 0:
            return 0
        return (part / whole) * 100

    qualified_percentage = calculate_percentage(context['qualified'], context['total'])
    disqualified_percentage = calculate_percentage(context['disqualified'], context['total'])
    pending_percentage = calculate_percentage(context['pending'], context['total'])
    callback_percentage = calculate_percentage(context['callback'], context['total'])

    # Format percentages
    def format_percentage(value):
        return '{:.2f}'.format(value).rstrip('0').rstrip('.')

    context['qualified_perc'] = format_percentage(qualified_percentage)
    context['disqualified_perc'] = format_percentage(disqualified_percentage)
    context['pending_perc'] = format_percentage(pending_percentage)
    context['callback_perc'] = format_percentage(callback_percentage)


    
    


    


    return render(request, 'leads/my_leads.html', context)





def lead_report(request, lead_id):

    context = {}

    context['profile'] = Profile.objects.get(user=request.user)

    lead = Lead.objects.get(lead_id=lead_id,active=True)
    context['campaigns'] = Campaign.objects.filter(status="active")
    context['contactlists'] = ContactList.objects.filter(active=True)

    context['lead'] = lead

    context['agent_profile'] = lead.agent_profile
    context['property_types'] = PROPERTY_CHOICES
    context['timelines'] = TIMELINE_CHOICES
    context['lead_status'] = LEAD_CHOICES



    
    
    

    if request.method == "POST":

        data = request.POST
        

        total_percentage = data.get('hidden_total_percentage')


        lead = Lead.objects.get(lead_id=lead_id)

        if lead.status == "pending":

        
            dialer_list = data.get('dialer_list')
            contact_list = ContactList.objects.get(id=dialer_list)
            lead.contact_list = contact_list
            lead.seller_name = data.get('owner_name')
            lead.seller_phone = data.get('phone_number')
            lead.seller_email = data.get('email')
            lead.property_type = data.get('property_type')
            lead.property_address = data.get('address')
            lead.asking_price = data.get('asking_price')
            lead.market_value = data.get('market_value')
            lead.reason = data.get('reason')
            lead.timeline = data.get('timeline')
            lead.property_url = data.get('zillow_url')
            lead.callback = data.get('callback_time')
            lead.general_info = data.get('general_info')
            lead.extra_notes = data.get('extra_info')

            lead.quality_notes = data.get('quality_notes')
            lead.save()

        return redirect('/my-leads')


        
    return render(request, 'leads/lead_report.html', context)




@login_required
def leads_quality(request):
    context = {}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile


    negative_threshold = settings.negative_percentage
    neutral_threshold = settings.neutral_percentage

    now = tz.now()
    current_year = now.year
    current_month = now.month
    month_name = now.strftime('%B')
    context['month_name'] = month_name
    context['current_year'] = current_year
    leads = Lead.objects.filter(agent_profile=profile,
                    pushed__year=current_year,
                    pushed__month=current_month).exclude(status="pending").order_by('-pushed')
    
    context['contacts'] = leads[:10]
    lead_flows = list(leads.values_list('lead_flow', flat=True))
    total_count = len(lead_flows)

    negative_count = sum(1 for flow in lead_flows if flow < negative_threshold)
    neutral_count = sum(1 for flow in lead_flows if negative_threshold <= flow < neutral_threshold)
    positive_count = sum(1 for flow in lead_flows if flow >= neutral_threshold)

    
    negative_percentage = round((negative_count / total_count * 100),2) if total_count > 0 else 0
    neutral_percentage = round((neutral_count / total_count * 100),2) if total_count > 0 else 0
    positive_percentage = round((positive_count / total_count * 100),2) if total_count > 0 else 0

    context.update({
        'negative_count': negative_count,
        'neutral_count': neutral_count,
        'positive_count': positive_count,
        'negative_percentage': negative_percentage,
        'neutral_percentage': neutral_percentage,
        'positive_percentage': positive_percentage,
    })
    
    return render(request,'leads/leads_quality.html',context)




@login_required
def lead_scoring(request):
    context = {"settings": settings}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile

    now = tz.now()
    current_year = now.year
    current_month = now.month
    month_name = now.strftime('%B')
    context['month_name'] = month_name
    # Get the first and last days of the month
    first_day = datetime(current_year, current_month, 1)
    if current_month == 12:
        last_day = datetime(current_year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = datetime(current_year, current_month + 1, 1) - timedelta(days=1)

    # Get ISO week numbers for the first and last days of the month
    first_week = first_day.isocalendar()[1]
    last_week = last_day.isocalendar()[1]

    # Initialize a dictionary to store total points per week
    weekly_points_count = defaultdict(int)

    # Get leads for the current month and year
    leads = Lead.objects.filter(
        agent_profile=profile,
        status="qualified",
        pushed__year=current_year,
        pushed__month=current_month
    )
    
    context['leads'] = leads.order_by("-pushed")[:10]
    # Calculate lead points per campaign
    leads_per_campaign = leads.values('campaign').annotate(lead_count=Count('lead_id')).order_by('campaign')
    campaign_leads_count = {
        Campaign.objects.get(pk=item['campaign']).lead_points: item['lead_count']
        for item in leads_per_campaign
    }

    # Sum points for each week
    for lead in leads:
        week_number = lead.pushed.isocalendar()[1]  # Get ISO week number
        lead_points = Campaign.objects.get(pk=lead.campaign_id).lead_points
        weekly_points_count[week_number] += lead_points

    # Ensure that all weeks from first to last are represented
    weeks_in_month = range(first_week, last_week + 1)

    # Prepare list with total points for each week
    weekly_total_points_list = [weekly_points_count.get(week, 0) for week in weeks_in_month]

    # Convert week numbers to "Week 1", "Week 2", etc.
    week_labels = [f"Week {i + 1}" for i in range(len(weeks_in_month))]

    # Update context with week labels and total points per week
    context['week_numbers'] = week_labels
    context['weekly_total_points'] = weekly_total_points_list




    return render(request, 'leads/lead_scoring.html', context)




@login_required
def leads_leaderboard(request):
    context = {"settings": settings}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile

    now = tz.now()
    current_year = now.year
    current_month = now.month
    month_name = now.strftime('%B')
    context['month_name'] = month_name
    # Get the first and last days of the month
    role = Role.objects.get(role_name='Admin')
    active_coldcallers = Profile.objects.filter(active=True, role=role)

    # Initialize leaderboard
    leaderboard = []

    for agent in active_coldcallers:
        # Step 2: Fetch and aggregate qualified leads for the agent
        leads = Lead.objects.filter(
            agent_profile=agent,
            pushed__year=current_year,
            pushed__month=current_month,
            status="qualified"
        )

        # Aggregate lead points per campaign for this agent
        leads_per_campaign = leads.values('campaign').annotate(lead_count=Count('lead_id'))

        # Step 3: Calculate total points for this agent
        total_points = 0
        for item in leads_per_campaign:
            campaign = Campaign.objects.get(pk=item['campaign'])
            total_points += campaign.lead_points * item['lead_count']

        # Add agent and their total points to the leaderboard
        leaderboard.append({'agent': agent, 'points': total_points})

    # Step 4: Sort the leaderboard by total points in descending order
    leaderboard = sorted(leaderboard, key=lambda x: x['points'], reverse=True)

    # Context for rendering
    context['leaderboard'] = leaderboard





    return render(request, 'leads/leaderboard.html', context)





def quality_pending(request):

    context = {}

    now = tz.now()
    current_year = now.year
    current_month = now.month
    current_month_name = _date(now, "F")
    
    context['year'] = current_year
    context['month_name'] =current_month_name

    


    context['profile'] = Profile.objects.get(user=request.user)
    context['pending_leads'] = Lead.objects.filter(status="pending", active=True).order_by('-pushed')[:10]

    context['qualified'] = Lead.objects.filter(
        pushed__month=current_month,
        pushed__year=current_year,
        status="qualified",
        active=True,
        handled_by=request.user,
        ).count()

    context['disqualified'] = Lead.objects.filter(
        pushed__month=current_month,
        pushed__year=current_year,
        status__in = ["disqualified", "duplicate"],
        active=True,
        handled_by=request.user,
        ).count()

    pending_leads = Lead.objects.filter(
        pushed__month=current_month,
        pushed__year=current_year,
        status="pending",
        active=True
        )
    
    context['pending'] = pending_leads.count()

    context['callback'] = Lead.objects.filter(
        pushed__month=current_month,
        pushed__year=current_year,
        status="callback",
        active=True,
        handled_by=request.user,
        ).count()


    context['total_handled_month'] =  Lead.objects.filter(
        pushed__month=current_month,
        pushed__year=current_year,
        status__in=['qualified','disqualified','duplicated','callback'],
        handled_by=request.user,
        active=True,
        ).count()
    
    context['total_month_all'] =  Lead.objects.filter(
        pushed__month=current_month,
        pushed__year=current_year,
        status__in=['qualified','disqualified','duplicated','callback'],
        active=True,
        ).count()
    
    if context['total_month_all'] == 0:
        context['total_handled_month_perc'] = 0  # or some other default value
    else:
        context['total_handled_month_perc'] = round((context['total_handled_month'] / context['total_month_all']) * 100, 2)


    context['total'] =  Lead.objects.filter(
        pushed__month=current_month,
        pushed__year=current_year,
        active=True,
        handled_by=request.user,
        ).count()
    
    context['total_year'] =  Lead.objects.filter(
        pushed__year=current_year,
        active=True,
        status__in=['qualified','disqualified','duplicated','callback'],
        handled_by=request.user,
        ).count()
    

    def calculate_percentage(part, whole):
        if whole == 0:
            return 0
        return (part / whole) * 100

    qualified_percentage = calculate_percentage(context['qualified'], context['total'])
    disqualified_percentage = calculate_percentage(context['disqualified'], context['total'])
    #pending_percentage = calculate_percentage(context['pending'], context['total'])
    callback_percentage = calculate_percentage(context['callback'], context['total'])

    # Format percentages
    def format_percentage(value):
        return '{:.2f}'.format(value).rstrip('0').rstrip('.')

    context['qualified_perc'] = format_percentage(qualified_percentage)
    context['disqualified_perc'] = format_percentage(disqualified_percentage)
    #context['pending_perc'] = format_percentage(pending_percentage)
    context['callback_perc'] = format_percentage(callback_percentage)

    char_data = []
    for month in range(1, 13):
        total_count = Lead.objects.filter(
            pushed__month=month,
            pushed__year=current_year,
            handled_by=request.user,
            status__in=['qualified','disqualified','duplicated','callback'],
            active=True
        ).count()
        char_data.append(total_count)
    context['char_data'] = char_data


    context['pending_leads'] =  Lead.objects.filter(
        status="pending",
        active=True
        )



    return render(request, "quality/pending_leads.html",context)





def quality_lead_reports(request):

    context = {}

    now = tz.now()
    current_year = now.year
    current_month = now.month
    current_month_name = _date(now, "F")
    
    context['year'] = current_year
    context['month_name'] =current_month_name

    


    context['profile'] = Profile.objects.get(user=request.user)

    context['qualified'] = Lead.objects.filter(
        pushed__year=current_year,
        agent_user=request.user,
        status="qualified",
        active=True
        ).count()

    context['disqualified'] = Lead.objects.filter(
        pushed__year=current_year,
        agent_user=request.user,
        status__in=["disqualified","callback"],
        active=True
        ).count()

    
    
    context['duplicated'] = Lead.objects.filter(
        pushed__year=current_year,
        agent_user=request.user,
        status="duplicated",
        active=True
        ).count()

    
    

    context['total'] =  Lead.objects.filter(
        pushed__year=current_year,
        agent_user=request.user,
        active=True
        ).count()
    

    

    char_data_qualified = []
    for month in range(1, 13):
        total_count = Lead.objects.filter(
            pushed__month=month,
            pushed__year=current_year,
            status="qualified",
            active=True
        ).count()
        char_data_qualified.append(total_count)
    context['char_data_qualified'] = char_data_qualified


    char_data_disqualified = []
    for month in range(1, 13):
        total_count = Lead.objects.filter(
            pushed__month=month,
            pushed__year=current_year,
            status="disqualified",
            active=True
        ).count()
        char_data_disqualified.append(total_count)
    context['char_data_disqualified'] = char_data_disqualified



        # Determine the first and last days of the current month
    first_day = datetime(current_year, current_month, 1)
    if current_month == 12:
        last_day = datetime(current_year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = datetime(current_year, current_month + 1, 1) - timedelta(days=1)

    # Get ISO week numbers for the first and last days of the month
    first_week = first_day.isocalendar()[1]
    last_week = last_day.isocalendar()[1]

    # Initialize a dictionary to store total leads per week
    weekly_leads_count = defaultdict(int)

    # Get leads for the current month and year
    leads = Lead.objects.filter(
        pushed__year=current_year,
        pushed__month=current_month,
        active=True
    )

    # Order and limit the number of leads in the context for display

    # Count total leads for each week
    for lead in leads:
        week_number = lead.pushed.isocalendar()[1]  # Get ISO week number
        weekly_leads_count[week_number] += 1

    # Ensure that all weeks from first to last are represented
    weeks_in_month = range(first_week, last_week + 1)

    # Prepare list with total leads for each week
    weekly_total_leads_list = [weekly_leads_count.get(week, 0) for week in weeks_in_month]

    # Convert week numbers to "Week 1", "Week 2", etc.
    week_labels = [f"Week {i + 1}" for i in range(len(weeks_in_month))]

    # Update context with week labels and total leads per week
    context['week_numbers'] = week_labels
    context['weekly_total_leads'] = weekly_total_leads_list


    qualified = Lead.objects.filter(
        pushed__month=current_month,
        pushed__year=current_year,
        status="qualified",
        active=True
        )
    
    qualified_dict = {
        str(lead.lead_id): {
            'longitude': lead.longitude,
            'latitude': lead.latitude,
            'seller_name': lead.seller_name
        }
        for lead in qualified
        if lead.longitude != 0 and lead.latitude != 0
    }
    context['locations'] = mark_safe(json.dumps(qualified_dict))

    state_lead_count = defaultdict(int)

    # Iterate through qualified leads and count by state
    for lead in qualified:
        state = lead.state
        state_lead_count[state] += 1

    # Convert defaultdict to a regular dict
    state_lead_count = dict(state_lead_count)

    # Sort states by lead count in descending order
    sorted_states = sorted(state_lead_count.items(), key=lambda x: x[1], reverse=True)

    # Initialize the dictionary for the top three and the remainder
    top_three_states = {}
    other_states_count = 0

    for i, (state, count) in enumerate(sorted_states):
        if i < 3:
            top_three_states[state] = count
        else:
            other_states_count += count

    # Add the "other states" to the dictionary
    if other_states_count > 0:
        top_three_states['Other'] = other_states_count

    # Update the context
    context['state_lead_count'] = top_three_states

    # Print the top three states and other states count
    


    context['all_leads'] = Lead.objects.filter(active=True).order_by('-pushed')
    
    
    



    return render(request, "quality/lead_reports.html",context)



@require_http_methods(["POST"])
def fire_lead(request, lead_id):
    try:
        lead = Lead.objects.get(lead_id=lead_id)
        lead.fireback = True
        lead.save()
        return JsonResponse({'message': 'Lead Fired successfully.'}, status=200)
    except lead.DoesNotExist:
        return JsonResponse({'message': 'Lead not found.'}, status=404)







def get_lead_status(request, lead_id):
    try:
        lead = Lead.objects.get(lead_id=lead_id)
        user_profile = Profile.objects.get(user=request.user)

        if lead.assigned:
            if lead.assigned == user_profile:
                return JsonResponse({'assigned_to_user': True})
            else:
                return JsonResponse({'assigned': True})
        
        if request.method == 'POST':
            lead.assigned = user_profile
            lead.assigned_time = tz.now()
            lead.save()
            return JsonResponse({'assigned': True})

        return JsonResponse({'assigned': False})
    except Lead.DoesNotExist:
        return JsonResponse({'error': 'Lead not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def lead_handling(request, lead_id):

    context = {}

    context['profile'] = Profile.objects.get(user=request.user)
    lead = Lead.objects.get(lead_id=lead_id,active=True)
    context['campaigns'] = Campaign.objects.filter(status="active")
    context['contactlists'] = ContactList.objects.filter(active=True)

    context['lead'] = lead

    context['agent_profile'] = lead.agent_profile
    context['property_types'] = PROPERTY_CHOICES
    context['timelines'] = TIMELINE_CHOICES
    context['lead_status'] = LEAD_CHOICES

    try:
        lead_flow_slots = LeadHandlingSettings.objects.get(active=True, campaign=lead.campaign)
        context['lead_flow_slots'] = lead_flow_slots.get_active_slots()
    except:
        context['lead_flow_slots'] = None

    


    if request.method == "POST":
        data = request.POST
        """slot_json = {}
        lead_flow_slots =lead_flow_slots.get_active_slots()
        for i in range(1, len(lead_flow_slots) + 1):
            slot_name = request.POST.get(f'slot{i}_name')
            slot_percentage = request.POST.get(f'slot{i}_percentage')
            # Ensure that slot_name is not empty and slot_percentage is not None
            if slot_name:
                # Access slot names directly from the dictionary
                slot_json[lead_flow_slots[i-1]['name']] = slot_percentage
        # Print or use the slot_dict as needed"""


        slot_json = {}
        lead_flow_slots = lead_flow_slots.get_active_slots()

        for i in range(1, len(lead_flow_slots) + 1):
            slot_name = request.POST.get(f'slot{i}_name')
            slot_percentage = request.POST.get(f'slot{i}_percentage')
            
            # Ensure that slot_name is not empty and slot_percentage is not None
            if slot_name and slot_percentage is not None:
                # Convert slot_percentage to float and make it negative if slot_name is '0'
                percentage_value = float(slot_percentage)
                if slot_name == '0':
                    percentage_value = -percentage_value
                
                # Access slot names directly from the dictionary
                slot_json[lead_flow_slots[i-1]['name']] = percentage_value

        # Print or use the slot_json as needed


        total_percentage = data.get('hidden_total_percentage')


        lead = Lead.objects.get(lead_id=lead_id)
        


        
        dialer_list = data.get('dialer_list')
        contact_list = ContactList.objects.get(id=dialer_list)
        lead.contact_list = contact_list
        lead.seller_name = data.get('owner_name')
        lead.seller_phone = data.get('phone_number')
        lead.seller_email = data.get('email')
        lead.property_type = data.get('property_type')
        lead.property_address = data.get('address')
        lead.asking_price = data.get('asking_price')
        lead.market_value = data.get('market_value')
        lead.reason = data.get('reason')
        lead.timeline = data.get('timeline')
        lead.property_url = data.get('zillow_url')
        lead.callback = data.get('callback_time')
        lead.general_info = data.get('general_info')
        lead.extra_notes = data.get('extra_info')

        lead.quality_notes = data.get('quality_notes')
        lead.lead_flow = float(total_percentage)
        lead.status = data.get('lead_status')
        lead.handled_by = request.user
        lead.lead_flow_json = slot_json
        lead.handled = tz.now()
        if not lead.handling_time:
            handling_time = tz.now() - lead.assigned_time
            lead.handling_time = handling_time
        lead.save()

        return redirect('/quality-pending')


        
    return render(request, 'quality/lead_handling.html', context)


@login_required
def feedbacks_table(request):

    context = {}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile
    context['feedbacks'] = Feedback.objects.filter(active=True).order_by('-created')


    return render(request,'quality/feedbacks.html',context)



@login_required
def feedback_single(request):


    context = {}
    profile = Profile.objects.get(user=request.user)


    context['profile'] = profile
    context['campaigns'] = Campaign.objects.filter(active=True)
    context['agent_profiles'] = Profile.objects.filter(active=True)



    if request.method == "POST":
        data = request.POST

        agent_id = data.get('agent')
        camp_id = data.get('campaign')
        phone_number = data.get('phone_number')
        feedback_type = data.get('feedback_type')
        feedback_text = data.get('feedback_text')

        if int(feedback_type) == 1:
            feedback_type = True
        else:
            feedback_type = False

        agent_profile = Profile.objects.get(id=agent_id)
        campaign = Campaign.objects.get(id=camp_id)

        feedback = Feedback.objects.create(agent=agent_profile.user,
                                agent_profile=agent_profile,
                                auditor=profile.user,
                                auditor_profile=profile,
                                phone=phone_number,
                                positive=feedback_type,
                                type="single",
                                feedback_text = feedback_text,

                                )
        feedback.campaign.add(campaign)

        return redirect('/feedbacks')

            
    
    return render(request,'quality/feedback_single.html',context)



@login_required
def feedback_multiple(request):


    context = {}
    profile = Profile.objects.get(user=request.user)


    context['profile'] = profile
    context['campaigns'] = Campaign.objects.filter(active=True)
    context['agent_profiles'] = Profile.objects.filter(active=True)



    if request.method == "POST":
        data = request.POST

        agent_id = data.get('agent')
        feedback_type = data.get('feedback_type')
        feedback_text = data.get('feedback_text')
        selected_camp_ids = data.getlist('campaigns')

        if int(feedback_type) == 1:
            feedback_type = True
        else:
            feedback_type = False

        agent_profile = Profile.objects.get(id=agent_id)
        camps = Campaign.objects.filter(id__in=selected_camp_ids)

        feedback = Feedback.objects.create(agent=agent_profile.user,
                                agent_profile=agent_profile,
                                auditor=profile.user,
                                auditor_profile=profile,
                                positive=feedback_type,
                                type="multiple",
                                feedback_text = feedback_text,

                                )
        feedback.campaign.add(*camps)
    

        return redirect('/feedbacks')

            
    
    return render(request,'quality/feedback_multiple.html',context)




@login_required
def feedback_report(request, id):


    context = {}
    profile = Profile.objects.get(user=request.user)


    context['profile'] = profile
    context['agent_profiles'] = Profile.objects.filter(active=True)
    context['feedback'] = Feedback.objects.get(id=id)
    context['feedback_status_choices'] = FEEDBACK_STATUS_CHOICES

    if request.method == "POST":
        data = request.POST
        feedback_id = data.get('feedback_id')
        feedback_status = data.get('feedback_status')
        feedback = Feedback.objects.get(id=id)
        feedback.status = feedback_status
        feedback.save()
        return redirect('/feedbacks')

            
    
    return render(request,'quality/feedback_report.html',context)

@login_required
def quality_agents(request):
    context = {"settings": settings}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile

    now = tz.now()
    current_year = now.year
    current_month = now.month
    month_name = now.strftime('%B')
    context['month_name'] = month_name
    # Get the first and last days of the month
    first_day = datetime(current_year, current_month, 1)
    if current_month == 12:
        last_day = datetime(current_year + 1, 1, 1) - timedelta(days=1)
    else:
        last_day = datetime(current_year, current_month + 1, 1) - timedelta(days=1)

    # Get ISO week numbers for the first and last days of the month
    first_week = first_day.isocalendar()[1]
    last_week = last_day.isocalendar()[1]

    # Initialize a dictionary to store the count of qualified leads per week
    weekly_leads_count = defaultdict(int)

    # Get leads for the current month and year
    leads = Lead.objects.filter(
        status="qualified",
        pushed__year=current_year,
        pushed__month=current_month
    )
    
    # Count leads per week
    for lead in leads:
        week_number = lead.pushed.isocalendar()[1]  # Get ISO week number
        weekly_leads_count[week_number] += 1

    # Ensure that all weeks from first to last are represented
    weeks_in_month = range(first_week, last_week + 1)

    # Prepare list with total leads count for each week
    weekly_total_leads_list = [weekly_leads_count.get(week, 0) for week in weeks_in_month]

    # Convert week numbers to "Week 1", "Week 2", etc.
    week_labels = [f"Week {i + 1}" for i in range(len(weeks_in_month))]

    # Update context with week labels and total leads per week
    context['week_numbers'] = week_labels
    context['weekly_total_leads'] = weekly_total_leads_list


    quality_teams = Team.objects.filter(team_type="quality")

    qa_reports = {}

    qa_agents = Profile.objects.filter(team__in=quality_teams)

    # Loop through each QA agent
    for qa_agent in qa_agents:
        # Aggregate leads data for the current QA agent
        aggregated_data = Lead.objects.filter(
            handled_by=qa_agent.user,
            pushed__year=current_year,
            pushed__month=current_month
        ).aggregate(
            qualified_count=Count('lead_id', filter=Q(status='qualified')),
            disqualified_count=Count('lead_id', filter=Q(status='disqualified')),
            handling_time_avg=Avg('handling_time'),
            total_leads_count=Count('lead_id'),
            fireback_count=Count('lead_id', filter=Q(fireback=True))
        )
        
        # Format the average handling time
        formatted_handling_time_avg = format_timedelta(aggregated_data['handling_time_avg'])
        
        # Store the results in the dictionary
        qa_reports[qa_agent] = {
            'qualified_count': aggregated_data['qualified_count'],
            'disqualified_count': aggregated_data['disqualified_count'],
            'handling_time_avg': formatted_handling_time_avg,
            'total_leads_count': aggregated_data['total_leads_count'],
            'fireback_count': aggregated_data['fireback_count']
        }

    context['qa_reports'] = qa_reports




    return render(request, 'quality/quality_agents.html', context)




def application_form(request):

    context = {}
    try:
        context['profile'] = Profile.objects.get(user=request.user)
    except:
        pass

    return render(request, 'applications/application_form.html', context)

@csrf_exempt
def handle_audio_upload(request):
    if request.method == 'POST' and request.FILES.get('audio_data'):
        audio_file = request.FILES['audio_data']
        try:
            # Example code to save file to media root
            new_application = Application(audio_file=audio_file)
            new_application.full_name = request.POST.get('full_name')
            new_application.position = request.POST.get('position')
            new_application.phone = request.POST.get('phone_number')
            new_application.email = request.POST.get('email')
            new_application.education = request.POST.get('education')
            new_application.start_date = request.POST.get('start_date')
            new_application.shift = request.POST.get('shift')
            new_application.experience = request.POST.get('previous_experience')
            new_application.save()
            return JsonResponse({'success': 'Application submitted successfully'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'No audio file found.'}, status=400)


@login_required
def upload_profile(request):
    if request.method == 'POST':
        if 'file' in request.FILES:
            file = request.FILES['file']
            # Check if the uploaded file is an image
            if file.content_type.startswith('image'):
                # Example: Save the file to a Profile model instance
                profile = Profile.objects.get(user=request.user)  # Adjust based on your profile retrieval logic
                profile.picture = file
                profile.save()
                return JsonResponse({'message': 'Image uploaded successfully.'})
            else:
                return JsonResponse({'error': 'File is not an image.'}, status=400)
        else:
            return JsonResponse({'error': 'File not provided.'}, status=400)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)


@login_required
def account_settings(request):
    context = {}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile


    return render(request,'users/settings.html', context)


@require_POST
def update_theme(request):
    data = json.loads(request.body)
    theme = data.get('theme')

    if theme == "dark":
        profile = Profile.objects.get(user=request.user)
        profile.settings_theme = "dark"
        profile.save()
    elif theme == "white":
        profile = Profile.objects.get(user=request.user)
        profile.settings_theme = "white"
        profile.save()

    return JsonResponse({'message': f'Theme updated to {theme}'})


@require_POST
def maps_theme(request):
    data = json.loads(request.body)
    theme = data.get('theme')

    if theme == "dark":
        profile = Profile.objects.get(user=request.user)
        profile.maps_theme = "dark"
        profile.save()
    elif theme == "white":
        profile = Profile.objects.get(user=request.user)
        profile.maps_theme = "white"
        profile.save()

    return JsonResponse({'message': f'Theme updated to {theme}'})


def payment_info(request):
    if request.method == 'POST':
        data = request.POST
        payoneer_account = data.get('payoneer_account')
        instapay_account = data.get('instapay_account')
        payoneer_choice = data.get('payoneer_choice')
        instapay_choice = data.get('instapay_choice')

        profile = Profile.objects.get(user=request.user)
        if profile.payoneer != payoneer_account:
            profile.payoneer = payoneer_account
        if profile.instapay != instapay_account:
            profile.instapay = instapay_account
        if payoneer_choice == "on":
            profile.payment_method = "payoneer"
        elif instapay_choice == "on":
            profile.payment_method = "instapay"
        else:
            redirect('/')
        profile.save()
    return redirect('/settings')




def address_autocomplete(request):

    if 'term' in request.GET:
        term = request.GET.get('term')
        HERE_API = django_settings.HERE_API
        url = f'https://autocomplete.geocoder.ls.hereapi.com/6.2/suggest.json?query={term}&apiKey={HERE_API}&country=USA'
        
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            suggestions = [item['label'] for item in data.get('suggestions', [])]
            return JsonResponse(suggestions, safe=False)
        else:
            return JsonResponse([], safe=False)
    return JsonResponse([], safe=False)



ALLOWED_EXTENSIONS = {
    'pdf': 'application/pdf',
    'doc': 'application/msword',
    'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'jpg': 'image/jpeg',
    'jpeg': 'image/jpeg',
    'png': 'image/png',
    'gif': 'image/gif',
    'mp4': 'video/mp4',
    'mov': 'video/quicktime',
    'avi': 'video/x-msvideo',
    # Add more video extensions if needed
}

MAX_FILE_SIZE_MB = 7

def validate_file(file):
    # Check file size
    if file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise ValidationError(f"File size exceeds {MAX_FILE_SIZE_MB} MB limit.")
    
    # Check file extension
    extension = file.name.split('.')[-1].lower()
    content_type = file.content_type
    
    if extension not in ALLOWED_EXTENSIONS:
        raise ValidationError("Unsupported file type.")
    
    # Check content type
    if content_type != ALLOWED_EXTENSIONS.get(extension):
        raise ValidationError("File type does not match its extension.")
   




@csrf_exempt
@login_required
def leave_request(request):
    context = {}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile
    context['leave_types'] = LEAVE_CHOICES

    if request.method == "POST":
        data = request.POST
        file = None
        agent_profile = Profile.objects.get(user=request.user)
        leave_type = data.get('leave_type')
        requested_date = data.get('requested_date')
        reason = data.get('reason')
 
        

        if 'file' in request.FILES:
            file = request.FILES['file']
            try:
                validate_file(file)
                
            except ValidationError as e:
                file= None

        # Create Leave instance with or without the file
        leave = Leave.objects.create(
            agent_user=request.user,
            agent_profile=agent_profile,
            agent_name=agent_profile.full_name,
            team=agent_profile.team,
            leave_type=leave_type,
            requested_date=requested_date,
            reason=reason,
            file=file if file else None  # Assign file only if it exists
        )

    
        

        return redirect('/leave-requests')
    return render(request,'requests/leave.html', context)



@login_required
def leave_request_list(request):
    context = {}
    profile = Profile.objects.get(user=request.user)
    context['leaves'] = Leave.objects.filter(active=True, agent_user=request.user).order_by('-submission_date')
    context['profile'] = profile

    return render(request,'requests/leaves_list.html', context)

@require_http_methods(["DELETE"])
def delete_leave(request, leave_id):
    try:
        leave = Leave.objects.get(id=leave_id)
        leave.delete()
        return JsonResponse({'message': 'Leave deleted successfully.'}, status=200)
    except Leave.DoesNotExist:
        return JsonResponse({'message': 'Leave not found.'}, status=404)






@login_required
def leave_handling_list(request):
    context = {}
    profile = Profile.objects.get(user=request.user)
    context['leaves'] = Leave.objects.filter(active=True).order_by('-submission_date')
    context['profile'] = profile

    return render(request,'requests/leaves_list_handling.html', context)



@login_required
def leave_report(request, leave_id):
    context = {}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile
    context['leave_types'] = LEAVE_CHOICES
    context['leave_status'] = REQUESTS_STATUS_CHOICES
    context['leave'] = Leave.objects.get(id=leave_id)
    context['teams'] = Team.objects.filter(active=True)

    if request.method == "POST":
        data = request.POST
        agent_profile = Profile.objects.get(user=request.user)
        leave_type = data.get('leave_type')
        requested_date = data.get('requested_date')
        reason = data.get('reason')
        status = data.get('leave_status')
 
        
        leave = Leave.objects.get(id=leave_id)

        leave.agent_user=request.user
        leave.agent_profile=agent_profile
        leave.agent_name=agent_profile.full_name
        leave.team=agent_profile.team
        leave.leave_type=leave_type
        leave.requested_date=requested_date
        leave.reason=reason
        leave.status=status
        leave.handled_by=request.user
        leave.save()
        if status == "approved":
            absence = Absence.objects.create(
                team = agent_profile.team,
                reporter = request.user,
                reporter_profile = agent_profile,
                agent = request.user,
                agent_profile = agent_profile,
                absence_date = requested_date,
                absence_type = leave_type,
                notes = reason,
            )
            
        

        return redirect('/leave-handling')
    return render(request,'requests/leave_report.html', context)







@csrf_exempt
@login_required
def action_request(request):
    context = {}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile
    context['action_types'] = ACTION_CHOICES

    if request.method == "POST":
        data = request.POST
        file = None
        userid = int(data.get('agentid'))
        agent_profile = Profile.objects.get(id=userid)
        action_type = data.get('action_type')
        incident_date = data.get('incident_date')
        deduction_amount = data.get('amount')
        reason = data.get('reason')
 
        

        if 'file' in request.FILES:
            file = request.FILES['file']
            try:
                validate_file(file)
                # Process file (save to database, etc.)
                # Example: save the file
                # YourModel.objects.create(file=file)
                pass
            except ValidationError as e:
                file = None

        # Create Leave instance with or without the file
        action = Action.objects.create(
            accuser=request.user,
            accuser_profile= Profile.objects.get(user=request.user),
            agent= agent_profile.user,
            agent_profile = agent_profile,
            action_type=action_type,
            incident_date=incident_date,
            deduction_amount=deduction_amount,
            reason=reason,
            file=file if file else None  # Assign file only if it exists
        )

        return redirect('/action-requests')
    return render(request,'requests/action.html', context)



@login_required
def action_request_list(request):
    context = {}
    profile = Profile.objects.get(user=request.user)
    context['actions'] = Action.objects.filter(active=True, accuser=request.user).order_by('-submission_date')
    context['profile'] = profile

    return render(request,'requests/actions_list.html', context)


@require_http_methods(["DELETE"])
def delete_action(request, action_id):
    try:
        action = Action.objects.get(id=action_id)
        action.delete()
        return JsonResponse({'message': 'Leave deleted successfully.'}, status=200)
    except Leave.DoesNotExist:
        return JsonResponse({'message': 'Leave not found.'}, status=404)






@login_required
def action_handling_list(request):
    context = {}
    profile = Profile.objects.get(user=request.user)
    context['actions'] = Action.objects.filter(active=True).order_by('-submission_date')
    context['profile'] = profile

    return render(request,'requests/action_list_handling.html', context)



@login_required
def action_report(request, action_id):
    context = {}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile
    context['action_types'] = ACTION_CHOICES
    context['action_status'] = REQUESTS_STATUS_CHOICES
    context['action'] = Action.objects.get(id=action_id)

    
    if request.method == "POST":
        data = request.POST
        action = Action.objects.get(id=action_id)
        userid = (action.agent_profile).id
        agent_profile = Profile.objects.get(id=userid)
        action_type = data.get('action_type')
        incident_date = data.get('incident_date')
        deduction_amount = data.get('amount')
        status = data.get('action_status')
        reason = data.get('reason')
 
        
        action = Action.objects.get(id=action_id)

        action.agent_user=request.user
        action.agent_profile=agent_profile
        action.agent_name=agent_profile.full_name
        action.team=agent_profile.team
        action.action_type=action_type
        action.incident_date=incident_date
        action.deduction_amount = deduction_amount
        action.reason=reason
        action.status=status
        action.handled_by=request.user
        action.save()
        

        return redirect('/action-handling')
    return render(request,'requests/action_report.html', context)



















def format_duration(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"



@login_required
def update_status(request):
    new_status = request.POST.get('status')
    user = request.user
    today = (tz.localtime(tz.now())).date()
    
    if new_status in dict(WorkStatus.STATUS_CHOICES).keys():
        try:
            work_status, created = WorkStatus.objects.get_or_create(
                user=user,
                date=today,
                defaults={
                    'current_status': 'ready',
                    'last_status_change': tz.now()
                }
            )
            if not created:
                work_status.update_status(new_status)
            
            # Calculate updated total times in seconds
            ready_time_seconds = work_status.ready_time.total_seconds()
            meeting_time_seconds = work_status.meeting_time.total_seconds()
            break_time_seconds = work_status.break_time.total_seconds()
            offline_time_seconds = work_status.offline_time.total_seconds()
            
            # Format times
            def format_duration(seconds):
                hours, remainder = divmod(seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

            # Prepare response
            response_data = {
                'success': True,
                'new_status': new_status,
                'ready_time': format_duration(ready_time_seconds),
                'meeting_time': format_duration(meeting_time_seconds),
                'break_time': format_duration(break_time_seconds),
                'offline_time': format_duration(offline_time_seconds),
                'last_status_change': work_status.last_status_change.isoformat()
            }
            return JsonResponse(response_data)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid status.'})





def work_status_data(request):
    today = (tz.localtime(tz.now())).date()
    user = request.user
    
    try:
        work_status = WorkStatus.objects.get(user=user, date=today)
    except WorkStatus.DoesNotExist:
        work_status = WorkStatus.objects.create(user=user, date=today, current_status='offline')

    # Calculate total times in seconds
    ready_time_seconds = work_status.ready_time.total_seconds()
    meeting_time_seconds = work_status.meeting_time.total_seconds()
    break_time_seconds = work_status.break_time.total_seconds()

    data = {
        'current_status': work_status.current_status,
        'ready_time': ready_time_seconds,
        'meeting_time': meeting_time_seconds,
        'break_time': break_time_seconds,
        'last_status_change': work_status.last_status_change.isoformat(),
    }
    return JsonResponse(data)