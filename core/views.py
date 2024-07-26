from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Application
from django.conf import settings as django_settings
from django.http import JsonResponse,HttpResponse
from django.core import serializers
from django.contrib.sessions.models import Session
from django.template.loader import render_to_string
from django.apps import apps
from .models import *
from datetime import datetime,timedelta
import json
from django.utils import timezone as tz
from itertools import chain
from operator import attrgetter
import calendar,time
from django.utils.timezone import now
import asyncio
from django.core.files.storage import default_storage
import os
import requests


try:
    settings = ServerSetting.objects.first()
except:
    settings = None






def loginview(request):
    context = {"settings":settings,}
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
    context = {"settings":settings,}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile
    return render(request,'dashboard/agent.html',context)

@login_required
def user_profile(request):
    context = {"settings":settings,}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile

    return render(request,'profile.html', context)

@login_required
def lead_submission(request):
    context = {"settings":settings,"api_token":django_settings.HERE_API}
    profile = Profile.objects.get(user=request.user)
    context['profile'] = profile
    if request.method == "POST":
        data = request.POST
        lat,long = data.get('latitude'),data.get('longitude')
        print(lat,long)    
    
    


    return render(request,'leads/lead_submission.html', context)




def application_form(request):

    context = {"settings":settings,}
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
    context = {"settings":settings,}
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


def test_view(request):
    """# Address you want to geocode
    address = "1970 Henry Rd, Conway"
    
    # HERE API credentials
    HERE_API = django_settings.HERE_API
    
    # HERE Geocoding API endpoint
    url = f"https://geocode.search.hereapi.com/v1/geocode?q={address}&apiKey={HERE_API}"
    
    try:
        # Perform GET request to HERE API
        response = requests.get(url)
        
        # Check if request was successful
        if response.status_code == 200:
            data = response.json()
            
            # Extract first result (assuming it's the most relevant)
            if data.get('items'):
                first_result = data['items'][0]
                position = first_result.get('position')
                
                if position:
                    # Extract latitude and longitude
                    lat = position['lat']
                    lon = position['lng']
                    
                    # Construct location object
                    location = {
                        'latitude': lat,
                        'longitude': lon,
                        'address': first_result.get('title', '')
                    }
                    
                    # Add geolocation data to context
                    context['location'] = location
                else:
                    print("No position data found in API response.")
            else:
                print("No 'items' found in API response.")
        else:
            print(f"Request failed with status code: {response.status_code}")
    
    except requests.RequestException as e:
        # Handle request exceptions (e.g., network issues)
        print(f"Error making request: {e}")"""
    return render(request, 'test.html')

