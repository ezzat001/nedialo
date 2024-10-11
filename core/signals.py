from django.dispatch import Signal, receiver
from django.utils import timezone
import threading
from django.contrib.auth import logout

import time
from .models import Profile, WorkStatus  # Import your Profile and WorkStatus models
import pytz
from datetime import datetime
from discord_app.bot import queue_message as discord_private
from discord_app.views import discord_crm_timeout

from .models import DialerCredentials,SeatAssignmentLog

# Signals for user heartbeat and timeout
user_heartbeat_signal = Signal()
user_timeout_signal = Signal()

# Store user last heartbeat timestamps and request data
user_last_seen = {}
user_requests = {}

# Timeout duration (5 minutes = 300 seconds)
TIMEOUT_DURATION = 300  # 5 minutes

def check_user_timeouts():
    while True:
        now = timezone.now()
        for user, last_seen in list(user_last_seen.items()):

            if (now - last_seen).total_seconds() > TIMEOUT_DURATION:
                # Send a timeout signal if the user has been inactive for too long
                user_timeout_signal.send(sender=None, user=user, request=user_requests.get(user))
                # Remove user from the tracking list
                del user_last_seen[user]
                if user in user_requests:
                    del user_requests[user]
        time.sleep(TIMEOUT_DURATION / 2)

# Start the timeout checking thread
thread = threading.Thread(target=check_user_timeouts)
thread.daemon = True
thread.start()

# Signal receiver to update user activity on heartbeat
@receiver(user_heartbeat_signal)
def update_user_last_seen(sender, user, request, **kwargs):
    user_last_seen[user] = timezone.now()
    user_requests[user] = request  # Store the request object

# Signal receiver to handle user timeout
@receiver(user_timeout_signal)
def handle_user_timeout(sender, user, request, **kwargs):
    profile = Profile.objects.get(user=user)
    today = (timezone.localtime(timezone.now())).date()

    work_status = WorkStatus.objects.filter(user=user, date=today).last()

    last_status = work_status.current_status
    if last_status != "offline":
        updated_count = WorkStatus.objects.filter(
        user=user,
        date=today
            ).update(
                current_status="offline",
                last_status_change=timezone.now()
            )
        
        try:
            seat = profile.assigned_credentials
            
            if seat:
                # Update the SeatAssignmentLog to end the session
                SeatAssignmentLog.objects.filter(
                    agent_profile=profile,
                    dialer_credentials=seat,
                    end_time__isnull=True
                ).update(end_time=timezone.now())

                # Clear the seat assignment for both the agent and the seat
                
        except DialerCredentials.DoesNotExist:
            pass  # Handle the case where the agent does not have an assigned seat



        try:
            message = "Your Connection Timed out from the CRM! Please Login back and re-set your working status."
            discord_private(int(profile.discord),message)
        except Exception as e:
            print(e)

        try:
            discord_crm_timeout(profile.full_name,request)
        except Exception as e:
            print(e)
        logout(request)

    

                

"""        if request:
            try:
                discord_crm_timeout(profile.full_name, request)
            except:
                pass

            message = "Your connection timed out from the CRM! Please log back in and reset your working status."

            try:
                discord_private(int(profile.discord), message)
            except Exception as e:
                print(e)

            logout(request)        # Send notification if request is available
"""
