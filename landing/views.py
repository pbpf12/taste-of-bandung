from landing.models import Suggestion
from landing.forms import SuggestionForm

from django.shortcuts import render
import smtplib
from email.message import EmailMessage
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.http import HttpResponse
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from django.core.paginator import Paginator



# Create your views here.
@login_required(login_url="login")
def show_landing(request):
    return render(request, "landing.html")
# Function to send an email

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse(''))
    response.delete_cookie('last_login')
    return response

def send_email(to_email, subject, body):
    # Create the email content
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = 'zillan.lambot@gmail.com'  # Your email address
    msg['To'] = to_email  # The recipient's email address
    msg.set_content(body)  # The body of the email

    # Connect to the Gmail SMTP server
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('zillan.lambot@gmail.com', 'your_password')  # Your email and app-specific password
            smtp.send_message(msg)  # Send the email

        print(f"Email sent to {to_email}!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")



@csrf_exempt
@require_POST
def add_suggestion_entry_ajax(request):
    suggestionMessage = strip_tags(request.POST.get("name"))
    # mood = strip_tags(request.POST.get("mood")) # strip HTML tags!
    # feelings = strip_tags(request.POST.get("feelings")) # strip HTML tags!

    new_suggestion = Suggestion(
        suggestionMessage = suggestionMessage
    )
    return HttpResponse(b"CREATED", status=201)