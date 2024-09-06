from django.shortcuts import render, redirect
from core.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone as tz
from collections import defaultdict
from django.db.models import Count
from django.views.decorators.http import require_POST
from datetime import datetime,timedelta
import calendar
import json


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




@login_required
def seat_breakdown(request, seat_id):
    context = {"settings":settings,}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile
    

    context['seat_logs'] = get_seat_breakdown(seat_id)

    context['seat'] = DialerCredentials.objects.get(id=seat_id)
    
    return render(request,'operations/seat_breakdown.html', context)



@login_required
def agent_seat_breakdown(request, agent_id):
    context = {"settings":settings,}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile
    

    context['seat_logs'] = get_agent_breakdown(agent_id)

    context['agent_profile'] = Profile.objects.get(id=agent_id)
    
    return render(request,'operations/agent_seat_breakdown.html', context)



def get_agent_breakdown(agent_profile_id):
    """Get a breakdown of all seat assignments for a specific agent."""
    seat_logs = SeatAssignmentLog.objects.filter(agent_profile_id=agent_profile_id)
    breakdown = []
    
    for log in seat_logs:
        breakdown.append({
            'seat_id': log.dialer_credentials.id,
            'seat_username':log.dialer_credentials.username,
            'campaign':log.dialer_credentials.campaign,
            'created_time':log.created_time,
            'start_time': log.start_time,
            'end_time': log.end_time,
            'duration_formatted': log.duration_formatted(),
        })
    
    return breakdown
def get_seat_breakdown(dialer_credentials_id):
    """Get a breakdown of all agent assignments for a specific seat."""
    seat_logs = SeatAssignmentLog.objects.filter(dialer_credentials_id=dialer_credentials_id)
    breakdown = []
    
    for log in seat_logs:
        breakdown.append({
            'agent_id': log.agent_profile.id,
            'agent_name':log.agent_profile.full_name,
            'start_time': log.start_time,
            'end_time': log.end_time,
            'created_time':log.created_time,
            'duration_formatted': log.duration_formatted(),
        })
    
    return breakdown

def list_all_agent_breakdowns():
    """List breakdowns for all agents."""
    all_breakdowns = []
    agents = Profile.objects.all()
    
    for agent in agents:
        breakdown = get_agent_breakdown(agent.id)
        all_breakdowns.append({
            'agent_id': agent.id,
            'breakdown': breakdown,
        })
    
    return all_breakdowns

def list_all_seat_breakdowns():
    """List breakdowns for all seats."""
    all_breakdowns = []
    seats = DialerCredentials.objects.all()
    
    for seat in seats:
        breakdown = get_seat_breakdown(seat.id)
        all_breakdowns.append({
            'seat_id': seat.id,
            'breakdown': breakdown,
        })
    
    return all_breakdowns



def update_seat_agent_profile(request, seat_id):
    if request.method == 'POST':
        # Check if the request is an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            agent_id = request.POST.get('agent_id')

            try:
                old_seat = None
                # Fetch the seat object
                seat = get_object_or_404(DialerCredentials, id=seat_id)

                if int(agent_id) == 0:
                    # Unassign the current agent from the seat
                    agent_profile = seat.agent_profile

                    if agent_profile:
                        # Log the end of the current session
                        SeatAssignmentLog.objects.filter(
                            agent_profile=agent_profile,
                            dialer_credentials=seat,
                            end_time__isnull=True
                        ).update(end_time=timezone.now())

                        # Update agent and seat profiles
                        agent_profile.assigned_credentials = None
                        agent_profile.save()

                    # Clear the seat's agent profile assignment
                    seat.agent_profile = None
                    seat.save()
                
                else:
                    # Assign a new agent to the seat
                    agent_profile = get_object_or_404(Profile, id=agent_id)

                    # Check if this agent is already assigned to a different seat
                    try:
                        old_seat = DialerCredentials.objects.get(agent_profile=agent_profile)

                        # Log the end of the session on the old seat
                        SeatAssignmentLog.objects.filter(
                            agent_profile=agent_profile,
                            dialer_credentials=old_seat,
                            end_time__isnull=True
                        ).update(end_time=timezone.now())

                        # Unassign the old seat
                        old_seat.agent_profile = None
                        old_seat.save()

                    except DialerCredentials.DoesNotExist:
                        # No previous seat assignment exists for this agent
                        pass

                    # Assign the new seat to the agent
                    seat.agent_profile = agent_profile
                    seat.save()

                    # Update the agent profile to reflect the new seat assignment
                    agent_profile.assigned_credentials = seat
                    agent_profile.save()

                    # Log the start of the new seat assignment session
                    SeatAssignmentLog.objects.create(
                        agent_profile=agent_profile,
                        dialer_credentials=seat,
                        start_time=timezone.now()
                    )

                # Return a successful response
                return JsonResponse({'success': True, 'message': 'Seat agent profile updated successfully.'})

            except Exception as e:
                # Return a failure response with the error message
                return JsonResponse({'success': False, 'message': str(e)})

    # If the request is not POST or not an AJAX request, return a 405 Method Not Allowed response
    return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=405)

@require_POST
def unseat_agent(request, agent_id):
    try:
        
        agent_profile = Profile.objects.get(id=agent_id)
        seat = agent_profile.assigned_credentials
        if agent_profile:
            # Log the end of the current session
            SeatAssignmentLog.objects.filter(
                agent_profile=agent_profile,
                dialer_credentials=seat,
                end_time__isnull=True
            ).update(end_time=timezone.now())

            # Update agent and seat profiles
            agent_profile.assigned_credentials = None
            agent_profile.save()

        # Clear the seat's agent profile assignment
        seat.agent_profile = None
        seat.save()

        return JsonResponse({'message': 'Agent unseated successfully.'}, status=200)

    except DialerCredentials.DoesNotExist:
        return JsonResponse({'message': 'Seat not found.'}, status=404)


"""
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
                return JsonResponse({'success': False, 'message': str(e)})"""
            
            





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










def calculate_working_days(month, year):
    # Get the total number of days in the given month and year
    total_days = calendar.monthrange(year, month)[1]
    
    working_days = 0
    
    for day in range(1, total_days + 1):
        date = datetime(year, month, day)
        # Check if the day is a weekday (Monday=0, ..., Sunday=6)
        if date.weekday() < 5:  # 0-4 corresponds to Monday-Friday
            working_days += 1
            
    return working_days

def calculate_working_days_in_year(year):
    """
    Calculate the number of working days (Monday through Friday) in the given year.
    """
    working_days = 0
    for month in range(1, 13):
        month_start_date = datetime(year, month, 1)
        if month == 12:
            month_end_date = datetime(year + 1, 1, 1) - timedelta(seconds=1)
        else:
            month_end_date = datetime(year, month + 1, 1) - timedelta(seconds=1)
        
        for single_date in (month_start_date + timedelta(n) for n in range((month_end_date - month_start_date).days + 1)):
            if single_date.weekday() < 5:  # Monday to Friday
                working_days += 1

    return working_days


def calculate_working_days_in_month(start_date, end_date):
    """
    Calculate the number of working days (Monday through Friday) in the given month.
    """
    working_days = 0
    for single_date in (start_date + timedelta(n) for n in range((end_date - start_date).days + 1)):
        if single_date.weekday() < 5:  # Monday to Friday
            working_days += 1

    return working_days




def format_hours_minutes(decimal_hours):
    """
    Convert decimal hours to HH:MM format.
    """
    hours = int(decimal_hours)
    minutes = int(round((decimal_hours - hours) * 60))
    return f"{hours:02}:{minutes:02}"


@login_required
def camp_hours_daily(request, camp_id, month, year):
    context = {"settings": settings}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile

    # Create a datetime object for the given month
    month_date = datetime(year, month, 1)
    month_name = month_date.strftime('%b')
    context['year'] = year
    context['month'] = month
    context['month_name'] = month_name
    context['full_month_name'] = calendar.month_name[month]
    
    campaign = Campaign.objects.get(id=camp_id)
    context['campaign'] = campaign

    working_days_in_month = calculate_working_days(month, year)
    target_hours_daily = campaign.weekly_hours / 5
    target_hours_monthly = target_hours_daily * working_days_in_month

    context['target_hours_daily'] = int(target_hours_daily)

    start_date = timezone.make_aware(datetime(year, month, 1))  # First day of the month
    if month == 12:
        end_date = timezone.make_aware(datetime(year + 1, 1, 1)) - timedelta(seconds=1)  # Last second of December
    else:
        end_date = timezone.make_aware(datetime(year, month + 1, 1)) - timedelta(seconds=1)  # Last second of the month

    # Initialize lists to hold days and durations
    days_list = []
    durations_list = []

    # Calculate daily accumulated durations
    current_date = start_date
    while current_date <= end_date:
        next_date = current_date + timedelta(days=1)
        accumulated_duration_seconds = campaign.get_accumulated_durations(current_date, next_date)
        
        # Convert accumulated seconds to decimal hours
        accumulated_hours_total = accumulated_duration_seconds / 3600  # Convert seconds to hours
        
        # Append day and duration to lists
        days_list.append(f"{current_date.day}")
        durations_list.append(f"{accumulated_hours_total:.2f}")  # Format as decimal hours
        
        # Move to the next day
        current_date = next_date

    # Calculate the total accumulated hours and achievement percentage
    total_accumulated_seconds = sum(
        campaign.get_accumulated_durations(datetime(year, month, int(day)), 
                                            datetime(year, month, int(day)) + timedelta(days=1))
        for day in days_list
    )
    accumulated_hours_total = total_accumulated_seconds / 3600  # Convert seconds to hours

    # Calculate achievement percentage
    achievement_percentage = (accumulated_hours_total / target_hours_monthly) * 100
    remaining_hours = target_hours_monthly - accumulated_hours_total

    # Format remaining hours in decimal hours
    remaining_hours = round(remaining_hours, 2)

    remaining_hours_percentage = (remaining_hours / target_hours_monthly) * 100

    # Format achieved hours in decimal hours
    achieved_hours_total = round(accumulated_hours_total, 2)
 
    formatted_remaining_hours = format_hours_minutes(remaining_hours)
    formatted_achieved_hours_total = format_hours_minutes(achieved_hours_total)

    # Add the formatted hours to the context
    context['remaining_hours_formatted'] = formatted_remaining_hours
    context['achieved_hours_formatted'] = formatted_achieved_hours_total


    # Add the new calculations to the context
    context['achievement_percentage'] = round(achievement_percentage, 2)
    context['remaining_hours_percentage'] = round(remaining_hours_percentage, 2)
    context['remaining_hours'] = remaining_hours
    context['achieved_hours'] = achieved_hours_total
    context['days_list'] = days_list
    context['durations_list'] = durations_list


    return render(request, 'campaign_hours/daily_reports.html', context)

@login_required
def camp_hours_monthly(request, camp_id, month, year):
    context = {"settings": settings}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile

    month_date = datetime(year, month, 1)  # Create a datetime object for the given month
    month_name = month_date.strftime('%b')  # Get the abbreviated month name (e.g., 'Sep')
    context['year'] = year
    context['month'] = month
    context['month_name'] = month_name
    context['full_month_name'] = calendar.month_name[month]
    campaign = Campaign.objects.get(id=camp_id)
    context['campaign'] = campaign

    working_days_in_month = calculate_working_days(month, year)

    target_hours_daily = campaign.weekly_hours / 5
    target_hours_monthly = target_hours_daily * working_days_in_month

    context['target_hours_monthly'] = int(target_hours_monthly)

    start_date = timezone.make_aware(datetime(year, month, 1))  # First day of the month
    if month == 12:
        end_date = timezone.make_aware(datetime(year + 1, 1, 1)) - timedelta(seconds=1)  # Last second of December
    else:
        end_date = timezone.make_aware(datetime(year, month + 1, 1)) - timedelta(seconds=1)  # Last second of the month

    # Get the accumulated duration for the specified month
    accumulated_duration_seconds = campaign.get_accumulated_durations(start_date, end_date)

    # Convert accumulated seconds to hours and minutes
    hours_accumulated, remainder = divmod(int(accumulated_duration_seconds), 3600)
    minutes_accumulated, _ = divmod(remainder, 60)

    # Format the accumulated time as HH:MM
    accumulated_duration_formatted = f"{hours_accumulated:02}:{minutes_accumulated:02}"

    # Calculate the percentage of target hours achieved
    accumulated_hours_total = accumulated_duration_seconds / 3600  # Convert seconds to hours
    achievement_percentage = (accumulated_hours_total / target_hours_monthly) * 100

    # Calculate remaining hours for the month
    remaining_hours = target_hours_monthly - accumulated_hours_total

    # Format remaining hours in HH:MM format
    remaining_hours_int = int(remaining_hours)
    remaining_minutes = int((remaining_hours - remaining_hours_int) * 60)
    remaining_hours_formatted = f"{remaining_hours_int:02}:{remaining_minutes:02}"

    remaining_hours_percentage = (remaining_hours / target_hours_monthly) * 100

    # Format achieved hours in HH:MM format
    achieved_hours_int = int(accumulated_hours_total)
    achieved_minutes = int((accumulated_hours_total - achieved_hours_int) * 60)
    achieved_hours_formatted = f"{achieved_hours_int:02}:{achieved_minutes:02}"

    # Add the new calculations to the context
    context['achievement_percentage'] = round(achievement_percentage, 2)
    context['remaining_hours_percentage'] = round(remaining_hours_percentage, 2)
    context['remaining_hours'] = round(remaining_hours, 2)  # This will give the remaining hours as a decimal
    context['remaining_hours_formatted'] = remaining_hours_formatted
    context['achieved_hours_formatted'] = achieved_hours_formatted

    # Initialize list to hold weekly hours
    weekly_hours = []
    weekly_hours_formatted = []  # Formatted weekly hours
    week_labels = []
    
    # Calculate weekly hours
    current_start_date = start_date
    while current_start_date <= end_date:
        current_end_date = current_start_date + timedelta(days=6)
        if current_end_date > end_date:
            current_end_date = end_date

        # Get the accumulated duration for the current week
        weekly_duration_seconds = campaign.get_accumulated_durations(current_start_date, current_end_date)
        weekly_hours_total = weekly_duration_seconds / 3600  # Convert seconds to hours

        # Convert weekly hours to HH:MM format
        hours, minutes = divmod(weekly_hours_total * 3600, 3600)
        formatted_hours = f"{int(hours):02}:{int(minutes / 60):02}"

        # Append numeric and formatted hours to lists
        weekly_hours.append(weekly_hours_total)
        weekly_hours_formatted.append(formatted_hours)

        # Label for the week
        week_labels.append(f"Week {len(week_labels) + 1}")

        # Move to the next week
        current_start_date = current_end_date + timedelta(days=1)

    # Add weekly hours and labels to the context
    context['week_labels'] = week_labels
    context['weekly_hours'] = weekly_hours
    context['weekly_hours_formatted'] = weekly_hours_formatted

    # Get total hours for each account
    account_data = campaign.get_total_hours_per_account(start_date, end_date)
    
    # Convert the account_data dictionary to a list of tuples
    account_hours_list = [(seat, data['formatted_time'], data['unique_agents_count']) 
                          for seat, data in account_data.items()]

    # Add account hours list to context
    context['account_hours_list'] = account_hours_list


    return render(request, 'campaign_hours/monthly_reports.html', context)








@login_required
def camp_hours_yearly(request, camp_id, year):
    context = {"settings": settings}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile
    context['year'] = year

    # Create a datetime object for January 1st of the given year
    year_start_date = timezone.make_aware(datetime(year, 1, 1))  # First day of the year
    year_end_date = timezone.make_aware(datetime(year + 1, 1, 1)) - timedelta(seconds=1)  # Last second of the year

    # Get the campaign for the given ID
    campaign = Campaign.objects.get(id=camp_id)
    context['campaign'] = campaign

    # Calculate total working days in the year (Monday to Friday)
    working_days_in_year = calculate_working_days_in_year(year)

    # Calculate target hours
    target_hours_daily = campaign.weekly_hours / 5  # Daily target hours (assuming 5 working days a week)
    target_hours_yearly = target_hours_daily * working_days_in_year

    context['target_hours_yearly'] = int(target_hours_yearly)

    # Get the accumulated duration for the specified year
    accumulated_duration_seconds = campaign.get_accumulated_durations(year_start_date, year_end_date)

    # Convert accumulated seconds to hours and minutes
    hours_accumulated, remainder = divmod(int(accumulated_duration_seconds), 3600)
    minutes_accumulated, _ = divmod(remainder, 60)

    # Format the accumulated time as HH:MM
    accumulated_duration_formatted = f"{hours_accumulated:02}:{minutes_accumulated:02}"

    # Calculate the percentage of target hours achieved
    accumulated_hours_total = accumulated_duration_seconds / 3600  # Convert seconds to hours
    achievement_percentage = (accumulated_hours_total / target_hours_yearly) * 100

    # Calculate remaining hours for the year
    remaining_hours = target_hours_yearly - accumulated_hours_total

    # Format remaining hours in HH:MM format
    remaining_hours_int = int(remaining_hours)
    remaining_minutes = int((remaining_hours - remaining_hours_int) * 60)
    remaining_hours_formatted = f"{remaining_hours_int:02}:{remaining_minutes:02}"

    remaining_hours_percentage = (remaining_hours / target_hours_yearly) * 100

    # Format achieved hours in HH:MM format
    achieved_hours_int = int(accumulated_hours_total)
    achieved_minutes = int((accumulated_hours_total - achieved_hours_int) * 60)
    achieved_hours_formatted = f"{achieved_hours_int:02}:{achieved_minutes:02}"

    # Add the new calculations to the context
    context['achievement_percentage'] = round(achievement_percentage, 2)
    context['remaining_hours_percentage'] = round(remaining_hours_percentage, 2)
    context['remaining_hours'] = round(remaining_hours, 2)  # This will give the remaining hours as a decimal
    context['remaining_hours_formatted'] = remaining_hours_formatted
    context['achieved_hours_formatted'] = achieved_hours_formatted

    # Initialize lists to hold monthly hours
    monthly_hours = []
    monthly_hours_formatted = []  # Formatted monthly hours
    month_labels = []
    missed_hours = []  # List to hold missed hours each month
    missed_hours_formatted = []  # Formatted missed hours each month

    # Calculate monthly hours and missed hours
    for month in range(1, 13):  # Loop through each month
        current_start_date = timezone.make_aware(datetime(year, month, 1))
        if month == 12:
            current_end_date = timezone.make_aware(datetime(year + 1, 1, 1)) - timedelta(seconds=1)
        else:
            current_end_date = timezone.make_aware(datetime(year, month + 1, 1)) - timedelta(seconds=1)

        # Get the accumulated duration for the current month
        monthly_duration_seconds = campaign.get_accumulated_durations(current_start_date, current_end_date)
        monthly_hours_total = monthly_duration_seconds / 3600  # Convert seconds to hours

        # Calculate the number of working days in the current month
        working_days_in_month = calculate_working_days_in_month(current_start_date, current_end_date)
        
        # Calculate the target hours for the current month
        target_hours_monthly = target_hours_daily * working_days_in_month

        # Calculate missed hours for the current month
        missed_hours_total = target_hours_monthly - monthly_hours_total

        # Convert monthly hours and missed hours to HH:MM format
        hours, minutes = divmod(monthly_hours_total * 3600, 3600)
        formatted_hours = f"{int(hours):02}:{int(minutes / 60):02}"
        missed_hours_int = int(missed_hours_total)
        missed_minutes = int((missed_hours_total - missed_hours_int) * 60)
        formatted_missed_hours = f"{missed_hours_int:02}:{missed_minutes:02}"

        # Append numeric and formatted hours to lists
        monthly_hours.append(monthly_hours_total)
        monthly_hours_formatted.append(formatted_hours)
        missed_hours.append(missed_hours_total)
        missed_hours_formatted.append(formatted_missed_hours)

        # Label for the month
        month_labels.append(calendar.month_name[month])

    # Add monthly hours, missed hours, and labels to the context
    context['month_labels'] = month_labels
    context['monthly_hours'] = monthly_hours
    context['monthly_hours_formatted'] = monthly_hours_formatted
    context['missed_hours'] = missed_hours
    context['missed_hours_formatted'] = missed_hours_formatted

    # Get total hours for each account
    account_data = campaign.get_total_hours_per_account(year_start_date, year_end_date)
    
    # Convert the account_data dictionary to a list of tuples
    account_hours_list = [(seat, data['formatted_time'], data['unique_agents_count']) 
                          for seat, data in account_data.items()]

    # Add account hours list to context
    context['account_hours_list'] = account_hours_list

    return render(request, 'campaign_hours/yearly_reports.html', context)




from django.utils import timezone
from datetime import datetime, timedelta
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import calendar
import json

@login_required
def camp_leads_daily(request, camp_id, month, year):
    context = {"settings": settings}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile

    # Get the campaign
    campaign = Campaign.objects.get(id=camp_id)
    context['campaign'] = campaign

    weekly_target = campaign.weekly_leads
    daily_target = weekly_target / 5  # 5 working days per week

    # Create a datetime object for the given month
    month_date = datetime(year, month, 1)
    month_name = month_date.strftime('%b')
    context['year'] = year
    context['month'] = month
    context['month_name'] = month_name
    context['full_month_name'] = calendar.month_name[month]

    # Create date range for the month
    start_date = timezone.make_aware(datetime(year, month, 1))  # First day of the month
    if month == 12:
        end_date = timezone.make_aware(datetime(year + 1, 1, 1)) - timedelta(seconds=1)  # Last second of December
    else:
        end_date = timezone.make_aware(datetime(year, month + 1, 1)) - timedelta(seconds=1)  # Last second of the month

    # Initialize lists for each lead status
    daily_qualified = []
    daily_disqualified = []
    daily_duplicated = []
    daily_callback = []
    day_labels = []

    # Initialize variables for total leads
    total_qualified = 0
    total_disqualified = 0
    total_duplicated = 0
    total_callback = 0

    # Loop through each day in the month
    current_date = start_date
    while current_date <= end_date:
        next_date = current_date + timedelta(days=1)
        
        # Query the leads for the current day in the campaign
        daily_leads = Lead.objects.filter(
            campaign=campaign,
            pushed__date=current_date.date()
        )
        
        # Filter by lead statuses
        qualified_leads = daily_leads.filter(status='qualified').count()
        disqualified_leads = daily_leads.filter(status='disqualified').count()
        duplicated_leads = daily_leads.filter(status='duplicated').count()
        callback_leads = daily_leads.filter(status="callback").count()

        # Append counts to the respective lists
        daily_qualified.append(qualified_leads)
        daily_disqualified.append(disqualified_leads)
        daily_duplicated.append(duplicated_leads)
        daily_callback.append(callback_leads)

        # Update total counts
        total_qualified += qualified_leads
        total_disqualified += disqualified_leads
        total_duplicated += duplicated_leads
        total_callback += callback_leads

        # Append day label
        day_labels.append(f"{current_date.day}")
        
        # Move to the next day
        current_date = next_date

    # Calculate the total number of working days in the month
    total_working_days = calculate_working_days_in_month(start_date, end_date)

    # Calculate the target leads for the month based on working days
    total_target_leads = daily_target * total_working_days

    # Add data to context
    context['day_labels'] = json.dumps(day_labels)
    context['daily_qualified'] = json.dumps(daily_qualified)
    context['daily_disqualified'] = json.dumps(daily_disqualified)
    context['daily_duplicated'] = json.dumps(daily_duplicated)
    context['daily_callback'] = json.dumps(daily_callback)

    # Calculate achievement percentage
    achievement_percentage = (total_qualified / total_target_leads) * 100 if total_target_leads > 0 else 0

    # Calculate remaining leads
    remaining_leads = total_target_leads - total_qualified

    # Calculate remaining percentage
    remaining_percentage = (remaining_leads / total_target_leads) * 100 if total_target_leads > 0 else 0

    # Format results
    context['daily_target'] = int(daily_target)
    context['achievement_percentage'] = round(achievement_percentage, 2)
    context['remaining_leads'] =  int(remaining_leads)
    context['achieved_leads'] = total_qualified
    context['remaining_percentage'] = round(remaining_percentage, 2)

    print(context)

    return render(request, 'campaign_leads/daily_reports.html', context)


@login_required
def camp_leads_monthly(request, camp_id, month, year):
    context = {"settings": settings}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile

    # Get the campaign
    campaign = Campaign.objects.get(id=camp_id)
    context['campaign'] = campaign

    weekly_target = campaign.weekly_leads
    daily_target = weekly_target / 5  # 5 working days per week

    
    month_date = datetime(year, month, 1)  # Create a datetime object for the given month
    month_name = month_date.strftime('%b')  # Get the abbreviated month name (e.g., 'Sep')
    context['year'] = year
    context['month'] = month
    context['month_name'] = month_name
    context['full_month_name'] = calendar.month_name[month]


    # Create date range for the month
    start_date = timezone.make_aware(datetime(year, month, 1))  # First day of the month
    if month == 12:
        end_date = timezone.make_aware(datetime(year + 1, 1, 1)) - timedelta(seconds=1)  # Last second of December
    else:
        end_date = timezone.make_aware(datetime(year, month + 1, 1)) - timedelta(seconds=1)  # Last second of the month

    # Calculate the total number of working days in the month
    total_working_days = calculate_working_days_in_month(start_date, end_date)
    
    # Calculate the target leads for the month based on working days
    total_target_leads = daily_target * total_working_days

    # Initialize lists for each lead status
    weekly_qualified = []
    weekly_disqualified = []
    weekly_duplicated = []
    weekly_callback = []
    week_labels = []

    # Initialize variables for total leads
    total_qualified = 0
    total_disqualified = 0
    total_duplicated = 0
    total_callback = 0

    # Loop through each week in the month
    current_start_date = start_date
    week_number = 1  # For labeling weeks
    while current_start_date <= end_date:
        current_end_date = current_start_date + timedelta(days=6)
        if current_end_date > end_date:
            current_end_date = end_date

        # Query the leads for the current week in the campaign
        weekly_leads = Lead.objects.filter(
            campaign=campaign,
            pushed__range=[current_start_date, current_end_date]
        )

        

        # Filter by lead statuses
        qualified_leads = weekly_leads.filter(status='qualified').count()
        disqualified_leads = weekly_leads.filter(status='disqualified').count()
        duplicated_leads = weekly_leads.filter(status='duplicated').count()
        callback_leads = weekly_leads.filter(status="callback").count()

        # Append counts to the respective lists
        weekly_qualified.append(qualified_leads)
        weekly_disqualified.append(disqualified_leads)
        weekly_duplicated.append(duplicated_leads)
        weekly_callback.append(callback_leads)

        # Update total counts
        total_qualified += qualified_leads
        total_disqualified += disqualified_leads
        total_duplicated += duplicated_leads
        total_callback += callback_leads

        # Append week label
        week_labels.append(f"Week {week_number}")
        week_number += 1

        # Move to the next week
        current_start_date = current_end_date + timedelta(days=1)

    # Add data to context
    context['week_labels'] = json.dumps(week_labels)
    context['weekly_qualified'] = json.dumps(weekly_qualified)
    context['weekly_disqualified'] = json.dumps(weekly_disqualified)
    context['weekly_duplicated'] = json.dumps(weekly_duplicated)
    context['weekly_callback'] = json.dumps(weekly_callback)

    # Calculate achievement percentage
    achievement_percentage = (total_qualified / total_target_leads) * 100 if total_target_leads > 0 else 0

    # Calculate remaining leads
    remaining_leads = total_target_leads - total_qualified

    # Calculate remaining percentage
    remaining_percentage = (remaining_leads / total_target_leads) * 100 if total_target_leads > 0 else 0

    # Format results
    context['total_target_leads'] = int(total_target_leads)
    context['achievement_percentage'] = round(achievement_percentage, 2)
    context['remaining_leads'] =  int(remaining_leads)
    context['achieved_leads'] = total_qualified
    context['remaining_percentage'] = round(remaining_percentage, 2)

    return render(request, 'campaign_leads/monthly_reports.html', context)




@login_required
def camp_leads_yearly(request, camp_id, year):
    context = {"settings": settings}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile
    context['year'] = year

    # Get the campaign for the given ID
    campaign = Campaign.objects.get(id=camp_id)
    context['campaign'] = campaign

    # Get the total number of working days in the year
    working_days_in_year = calculate_working_days_in_year(year)

    # Calculate weekly target leads
    weekly_target = campaign.weekly_leads
    daily_target = weekly_target / 5  # 5 working days per week
    total_target_leads_yearly = daily_target * working_days_in_year

    # Initialize lists for each month's data
    monthly_qualified = []
    monthly_disqualified = []
    monthly_duplicated = []
    monthly_callback = []
    month_labels = []
    
    total_qualified = 0
    total_disqualified = 0
    total_duplicated = 0
    total_callback = 0

    # Loop through each month in the year
    for month in range(1, 13):  # From January to December
        month_date = datetime(year, month, 1)
        month_name = month_date.strftime('%b')  # Abbreviated month name (e.g., 'Jan')
        month_labels.append(calendar.month_name[month])

        # Define the start and end dates for the current month
        start_date = timezone.make_aware(datetime(year, month, 1))  # First day of the month
        if month == 12:
            end_date = timezone.make_aware(datetime(year + 1, 1, 1)) - timedelta(seconds=1)  # Last second of December
        else:
            end_date = timezone.make_aware(datetime(year, month + 1, 1)) - timedelta(seconds=1)  # Last second of the month

        # Query the leads for the current month
        monthly_leads = Lead.objects.filter(
            campaign=campaign,
            pushed__range=[start_date, end_date]
        )

        # Filter by lead statuses
        qualified_leads = monthly_leads.filter(status='qualified').count()
        disqualified_leads = monthly_leads.filter(status='disqualified').count()
        duplicated_leads = monthly_leads.filter(status='duplicated').count()
        callback_leads = monthly_leads.filter(status="callback").count()

        # Append counts to the respective lists
        monthly_qualified.append(qualified_leads)
        monthly_disqualified.append(disqualified_leads)
        monthly_duplicated.append(duplicated_leads)
        monthly_callback.append(callback_leads)

        # Update total counts
        total_qualified += qualified_leads
        total_disqualified += disqualified_leads
        total_duplicated += duplicated_leads
        total_callback += callback_leads

    # Calculate annual statistics
    achievement_percentage = (total_qualified / total_target_leads_yearly) * 100 if total_target_leads_yearly > 0 else 0
    remaining_leads = total_target_leads_yearly - total_qualified
    remaining_percentage = (remaining_leads / total_target_leads_yearly) * 100 if total_target_leads_yearly > 0 else 0

    # Add data to context
    context['month_labels'] = month_labels
    context['monthly_qualified'] = json.dumps(monthly_qualified)
    context['monthly_disqualified'] = json.dumps(monthly_disqualified)
    context['monthly_duplicated'] = json.dumps(monthly_duplicated)
    context['monthly_callback'] = json.dumps(monthly_callback)
    
    context['total_target_leads_yearly'] = int(total_target_leads_yearly)
    context['total_qualified'] = total_qualified
    context['achievement_percentage'] = round(achievement_percentage, 2)
    context['remaining_leads'] = int(remaining_leads)
    context['remaining_percentage'] = round(remaining_percentage, 2)


    return render(request, 'campaign_leads/yearly_reports.html', context)
