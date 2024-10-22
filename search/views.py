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
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils.html import strip_tags
from django.core.paginator import Paginator
from search.models import *
from search.forms import *

@login_required(login_url="login")
def show_search_page(request):
    dishes = Dish.objects.all()

    context = {
        'dishes' : dishes
    }
    return render(request, 'search_page.html', context)

from django.shortcuts import render

@login_required(login_url="login")
def coba(request):
    movies = [
        {'title': 'Movie 1', 'description': 'This is movie 1.', 'color': 'bg-red-500'},
        {'title': 'Movie 2', 'description': 'This is movie 2.', 'color': 'bg-blue-500'},
        {'title': 'Movie 3', 'description': 'This is movie 3.', 'color': 'bg-green-500'},
        {'title': 'Movie 4', 'description': 'This is movie 4.', 'color': 'bg-yellow-500'},
        {'title': 'Movie 5', 'description': 'This is movie 5.', 'color': 'bg-purple-500'},
    ]
    return render(request, 'coba.html', {'movies': movies})

