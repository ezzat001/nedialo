from core.models import Team, ServerSetting, WorkStatus
from django.utils import timezone as tz
def global_context_processor(request):
    
    try:
        settings = ServerSetting.objects.first()
    except:
        settings = None

    teams = Team.objects.filter(team_type="callers") 

    user = request.user
    today = (tz.localtime(tz.now())).date()

    try:
        work_status = WorkStatus.objects.get(user=user, date=today)
    except:
        work_status = None

      


    context = {
                'callers_teams': teams,
                'settings':settings,
                "work_status":work_status,
               
               }
    return context