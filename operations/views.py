from django.shortcuts import render, redirect
from core.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone as tz
from collections import defaultdict
from django.db.models import Count


try:
    settings = ServerSetting.objects.first()
except:
    settings = None


@login_required
def seats(request):
    context = {"settings":settings,}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile
    campaigns = Campaign.objects.filter(active=True,status="active")
    context['campaigns'] = campaigns

    
    callers_teams = Team.objects.filter(team_type="callers")


    #callers = Profile.objects.filter(team__in=callers_teams,assigned_credentials__isnull=True, active=True)
    agents = Profile.objects.filter(team__in=callers_teams, active=True)
    #agents = 0 # CHECK CALLERS 
    context['agent_profiles'] = agents


    
    return render(request,'operations/seats.html', context)


def update_seat_agent_profile(request, seat_id):
    if request.method == 'POST':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            agent_id = request.POST.get('agent_id')
            


            try:
                old_seat = None
                seat = get_object_or_404(DialerCredentials, id=seat_id)
                if int(agent_id) == 0:

                    agent_profile = seat.agent_profile
                    agent_profile.assigned_credentials = None
                    seat.agent_profile = None
                else:
                    agent_profile = get_object_or_404(Profile, id=agent_id)
                    try:
                        old_seat = DialerCredentials.objects.get(agent_profile=agent_profile)
                        old_seat.agent_profile = None
                        old_seat.save()
                    except:
                        pass
                    seat.agent_profile = agent_profile
                    agent_profile.assigned_credentials = seat
                
                
                agent_profile.save()
                seat.save()
                

                return JsonResponse({'success': True, 'message': 'Seat agent profile updated successfully.'})

            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)})
            
            





@login_required
def working_hours_company(request):

    context = {}
    now = tz.now()
    current_year = now.year
    current_month = now.month
    month_name = now.strftime('%B')
    context['month_name'] = month_name
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile

    callers_teams = Team.objects.filter(team_type="callers")

    context['agents'] = Profile.objects.filter(team__in=callers_teams, active=True)
                                                   


    return render(request,'operations/working_hours.html',context)




@login_required
def working_hours_team(request, team_id):

    context = {}
    now = tz.now()

    month_name = now.strftime('%B')
    context['month_name'] = month_name
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile

    team = Team.objects.get(id=team_id)

    context['agents'] = Profile.objects.filter(team=team, active=True)
                                                   


    return render(request,'operations/working_hours.html',context)




@login_required
def agent_hours(request, agent_id):

    context = {}

    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile

    agent_profile = Profile.objects.get(id=agent_id)
    agent_user = agent_profile.user
    context['agent'] = agent_profile

    context['breakdown_data'] = WorkStatus.objects.filter(user=agent_user)
    
                                                   


    return render(request,'operations/agent_breakdown.html',context)






@login_required
def attendance_company(request):

    context = {}

    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile
    now = tz.now()
    current_year = now.year
    current_month = now.month
    month_name = now.strftime('%B')
    context['month_name'] = month_name
    context['today_date'] = now.date()

    context['absences'] = Absence.objects.filter(active=True)

    absence_counts = Absence.objects.filter(
        active=True,
        absence_date__month=current_month,
        absence_date__year=current_year,
    ).values('absence_type').annotate(count=Count('id'))

    # Initialize all counts to zero
    context['annuals'] = 0
    context['upls'] = 0
    context['sicks'] = 0
    context['casuals'] = 0
    context['nsncs'] = 0

    # Map the counts to the context dictionary
    for absence in absence_counts:
        if absence['absence_type'] == 'annual':
            context['annuals'] = absence['count']
        elif absence['absence_type'] == 'upl':
            context['upls'] = absence['count']
        elif absence['absence_type'] == 'sick':
            context['sicks'] = absence['count']
        elif absence['absence_type'] == 'casual':
            context['casuals'] = absence['count']
        elif absence['absence_type'] == 'nsnc':
            context['nsncs'] = absence['count']


    return render(request,'operations/attendance.html',context)



@login_required
def attendance_team(request, team_id):

    context = {}

    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile
    now = tz.now()
    current_year = now.year
    current_month = now.month
    month_name = now.strftime('%B')
    context['month_name'] = month_name
    context['today_date'] = now.date()
    team = Team.objects.get(id=team_id)

    context['absences'] = Absence.objects.filter(team = team, active=True)


    absence_counts = Absence.objects.filter(
        team = team,
        active=True,
        absence_date__month=current_month,
        absence_date__year=current_year,
    ).values('absence_type').annotate(count=Count('id'))

    # Initialize all counts to zero
    context['annuals'] = 0
    context['upls'] = 0
    context['sicks'] = 0
    context['casuals'] = 0
    context['nsncs'] = 0

    # Map the counts to the context dictionary
    for absence in absence_counts:
        if absence['absence_type'] == 'annual':
            context['annuals'] = absence['count']
        elif absence['absence_type'] == 'upl':
            context['upls'] = absence['count']
        elif absence['absence_type'] == 'sick':
            context['sicks'] = absence['count']
        elif absence['absence_type'] == 'casual':
            context['casuals'] = absence['count']
        elif absence['absence_type'] == 'nsnc':
            context['nsncs'] = absence['count']


    return render(request,'operations/attendance.html',context)




@login_required
def report_absence(request):

    context = {}

    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile
    now = tz.now()
    current_year = now.year
    current_month = now.month
    month_name = now.strftime('%B')
    context['month_name'] = month_name
    context['today_date'] = now.date()

    context['agents'] = Profile.objects.filter(active=True)

    context['absence_types'] = ABSENCE_CHOICES

    if request.method == "POST":
        data = request.POST
        next_url = request.GET.get('next', '/')  # Default URL if `next` is not provided

        agent_id = data.get('agent_id') 
        absence_type = data.get('absence_type')
        date = data.get('date')
        notes = data.get('notes')

        agent_profile = Profile.objects.get(id=agent_id)
        reporter_profile = Profile.objects.get(user=request.user)

        absence = Absence.objects.create(
            team = agent_profile.team,
            reporter = request.user,
            reporter_profile = reporter_profile,
            agent = agent_profile.user,
            agent_profile = agent_profile,
            absence_date = date,
            absence_type = absence_type,
            notes = notes,
        )
        return redirect(next_url)


    return render(request,'operations/report_absence.html',context)