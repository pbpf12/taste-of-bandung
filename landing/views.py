from landing.models import Suggestion
from landing.forms import SuggestionForm
from main.models import Dish

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
from django.db.models import Count
from django.db.models import Avg, Count

# Create your views here.
@login_required(login_url="login")
def show_landing(request):
    # Annotate each dish with the number of reviews and the average rating from reviews
    top_dishes = Dish.objects.order_by('-average_rating')[:3]

    # Prepare the context to pass to the template
    context = {
        'name': request.user.username,  # User's name
        'top_dishes': top_dishes,  # Top-rated dishes
    }

    # If no top dishes exist, you can still pass an optional message
    if not top_dishes.exists():
        context['message'] = "No dishes found with ratings yet."
        print("No dishes found with ratings yet.")  # Log to CMD if no dishes

    return render(request, "landing.html", context)
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
    msg['From'] = 'pbp2024f12@gmail.com'  # Your email address
    msg['To'] = to_email  # The recipient's email address
    msg.set_content(body)  # The body of the email

    # Connect to the Gmail SMTP server
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login('pbp2024f12@gmail.com', 'ioga xnqe snxl ybbb')  # Your email and app-specific password
            smtp.send_message(msg)  # Send the email

        print(f"Email sent to {to_email}!")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")



# @csrf_exempt
# @require_POST
# def add_suggestion_entry_ajax(request):
#     suggestionMessage = strip_tags(request.POST.get("name"))
#     # mood = strip_tags(request.POST.get("mood")) # strip HTML tags!
#     # feelings = strip_tags(request.POST.get("feelings")) # strip HTML tags!

#     new_suggestion = Suggestion(
#         suggestionMessage = suggestionMessage
#     )
#     new_suggestion.save() 
#     print(new_suggestion.suggestionMessage)

#     send_email('pbp2024f12@gmail.com','Suggestion From User',new_suggestion)
#     return HttpResponse(b"CREATED", status=201)

@csrf_exempt
@require_POST
def add_suggestion_entry_ajax(request):
    
    suggestionMessage = strip_tags(request.POST.get("suggestion"))
    print(suggestionMessage)
    
    if not suggestionMessage:
        print("none detected")
        return HttpResponse(b"Bad Request: Suggestion message is required", status=400)

    new_suggestion = Suggestion(suggestionMessage=suggestionMessage)
    new_suggestion.save()  # Save the new suggestion to the database

    send_email('pbp2024f12@gmail.com', 'Suggestion From User', suggestionMessage)
    return HttpResponse(b"CREATED", status=201)


def top_rated_dishes(request):
    # Annotate each dish with the number of reviews, then order by both average_rating and review count
    top_dishes = Dish.objects.annotate(review_count=Count('reviews')).order_by('-average_rating', '-review_count')[:3]

    # Check if there are any dishes with reviews
    if top_dishes.exists():
        context = {'top_dishes': top_dishes}
    else:
        print("none dishes")
        context = {'message': 'No dishes found with ratings yet.'}

    return render(request, 'landing.html', context) 