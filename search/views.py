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

def get_dishes(request):
    if request.method == "POST":
        form = SearchForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data.get('name')
            dish_type = form.cleaned_data.get('type')
            price_min = form.cleaned_data.get('price_min')
            price_max = form.cleaned_data.get('price_max')
            category = form.cleaned_data.get('category')
            sort_by = form.cleaned_data.get('sort_by')

            # Mulai filter queryset
            dishes = Dish.objects.all()

            if name:
                dishes = dishes.filter(name__icontains=name)

            if dish_type:
                dishes = dishes.filter(type__icontains=dish_type)

            if price_min is not None:
                dishes = dishes.filter(price__gte=price_min)

            if price_max is not None:
                dishes = dishes.filter(price__lte=price_max)

            if category:
                dishes = dishes.filter(category__icontains=category)

            # Sort dishes (if applicable)
            if sort_by:
                if sort_by == "cheapest":
                    dishes = dishes.order_by('price')
                elif sort_by == "most_expensive":
                    dishes = dishes.order_by('-price')

            # Serialisasi data ke JSON
            json_data = serializers.serialize("json", dishes)
            return HttpResponse(json_data, content_type="application/json")

    return HttpResponse("Invalid Request", status=400)