import json
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
from main.models import *
from search.forms import *

@login_required(login_url="login")
def show_search_page(request):
    dishes = Dish.objects.all()

    context = {
        'dishes' : dishes
    }
    return render(request, 'search_page.html', context)

def get_all_dishes(request):
    try:
        # Get all dishes
        dishes = Dish.objects.all()
        
        # Convert queryset to a list of dictionaries
        data = list(dishes.values(
            'id',
            'restaurant__name',
            'name',
            'description',
            'price',          # Ensure price is fetched
            'image',          # Ensure image is fetched
            'bookmark_count', # Ensure bookmark_count is fetched
            'average_rating'  # Include average_rating if needed
        ))

        # Return data as JSON response
        context = {
            'dishes': data,  # List of dictionaries
        }

        return JsonResponse(context)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def get_dishes(request):
    if request.method == "POST":
        # Mengambil JSON dari request body
        data = json.loads(request.body.decode('utf-8'))
        
        form = SearchForm(data)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            category = form.cleaned_data.get('category')
            price_min = form.cleaned_data.get('price_min')
            price_max = form.cleaned_data.get('price_max')
            sort_by = form.cleaned_data.get('sort_by')
            
            # Pagination data
            page_number = data.get('page', 1)  # Default to the first page
            
            # Mulai filter queryset
            dishes = Dish.objects.all()

            if name:
                dishes = dishes.filter(name__icontains=name)

            if category:
                dishes = dishes.filter(category=category)

            # Filter berdasarkan harga minimal dan maksimal secara bersamaan
            if price_min is not None and price_max is not None:
                dishes = dishes.filter(price__gte=price_min, price__lte=price_max)
            elif price_min is not None:
                dishes = dishes.filter(price__gte=price_min)
            elif price_max is not None:
                dishes = dishes.filter(price__lte=price_max)

            # Sort dishes (if applicable)
            if sort_by:
                if sort_by == "cheapest":
                    dishes = dishes.order_by('price')
                elif sort_by == "most_expensive":
                    dishes = dishes.order_by('-price')

            # Pagination logic
            paginator = Paginator(dishes, 10)  # Pagination with given items per page
            try:
                page_obj = paginator.page(page_number)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)

            # Serializing data
            data = list(page_obj.object_list.values(
                'id',
                'restaurant__name',
                'name',
                'description',
                'price',
                'image',
                'bookmark_count',
                'average_rating'
            ))

            # Provide pagination info
            context = {
                'dishes': data,
                'current_page': page_number,
                'min_page': 1,
                'max_page': paginator.num_pages,
            }

            return JsonResponse(context, safe=False)

    return HttpResponse("Invalid Request", status=400)
