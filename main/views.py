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
def main1(request):
    return render(request, "main1.html")

@login_required(login_url="login")
def main2(request):
    return render(request, "main2.html")

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse(''))
    response.delete_cookie('last_login')
    return response