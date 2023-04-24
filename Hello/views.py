from django.shortcuts import render,HttpResponse
from datetime import datetime
from django.http import JsonResponse
from home.models import Contact
from django.contrib import messages
from django.shortcuts import redirect
from django.views import View
from django.conf import settings
import requests
# Create your views here.
# def index(request):
#     messages.success(request,'This is root page')
#     return render(request,"index.html")

# def about(request):
#     return render(request,"about.html")

# def services(request):
#     return render(request,"services.html")

# def index(request):
#     return render(request,".html")
# def about(request):
#     return HttpResponse("this is About")
def contact(request):
    if request.method=="POST":
        n=request.POST.get('name1')
        e=request.POST.get('email')
        g=request.POST.get("gender")
        d=request.POST.get('desc')
        con=Contact(name=n,email=e,gender=g,desc=d,date=datetime.today())
        con.save()
        messages.success(request,'Your message has been sent')
    return render(request,"contact.html")


class GoogleCalendarInitView(View):
    def get(self, request):
        # Set the necessary parameters for the OAuth process
        client_id = settings.GOOGLE_CLIENT_ID
        redirect_uri = settings.GOOGLE_REDIRECT_URI
        scope = 'https://www.googleapis.com/auth/calendar'
        
        # Redirect the user to the Google authorization endpoint
        auth_url = f'https://accounts.google.com/o/oauth2/auth?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&response_type=code'
        return redirect(auth_url)

class GoogleCalendarRedirectView(View):
    def get(self, request):
        # Get the code from the request
        code = request.GET.get('code')
        
        # Set the necessary parameters for getting the access_token
        client_id = settings.GOOGLE_CLIENT_ID
        client_secret = settings.GOOGLE_CLIENT_SECRET
        redirect_uri = settings.GOOGLE_REDIRECT_URI
        grant_type = 'authorization_code'
        
        # Make a POST request to the Google token endpoint
        token_url = 'https://accounts.google.com/o/oauth2/token'
        data = {
            'code': code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'grant_type': grant_type
        }
        response = requests.post(token_url, data=data)
        access_token = response.json().get('access_token')
        
        # Use the access_token to get the list of events in the user's calendar
        calendar_url = 'https://www.googleapis.com/calendar/v3/calendars/primary/events'
        headers = {
            'Authorization': f'Bearer {access_token}'
        }
        events_response = requests.get(calendar_url, headers=headers)
        events = events_response.json().get('items', [])
        
        # Return the list of events in the response
        return JsonResponse(events, safe=False)        
