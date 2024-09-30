from core.models import Team, ServerSetting, WorkStatus, Campaign
from django.utils import timezone as tz
def global_context_processor(request):
    
    try:
        settings = ServerSetting.objects.first()
    except:
        settings = None

    callers_list = ['callers', 'sales']
    teams = Team.objects.filter(team_type__in=callers_list)

    user = request.user
    today = (tz.localtime(tz.now())).date()

    try:
        work_status = WorkStatus.objects.get(user=user, date=today)
    except:
        work_status = None

    callers_campaigns = Campaign.objects.filter(campaign_type="calling")
    now = tz.now()
    current_year = now.year
    current_month = now.month
    current_day = now.day

    sales_campaigns = Campaign.objects.filter(campaign_type="sales")


    context = {
                'callers_teams': teams,
                'settings':settings,
                "work_status":work_status,
                'callers_campaigns':callers_campaigns,
                'sales_campaigns':sales_campaigns,
                'current_year':current_year,
                'current_month':current_month,
                'current_day':current_day,
               
               }
    return context