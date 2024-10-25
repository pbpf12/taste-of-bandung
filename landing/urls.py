from django.shortcuts import redirect
from django.urls import path
from .views import *
from django.urls import path, include 

app_name = 'landing'

urlpatterns = [
    path('landing', show_landing, name='landing'),
    path('create-suggestion-entry-ajax', add_suggestion_entry_ajax, name='add_suggestion_entry_ajax'),
    path('top-rated-dishes/', top_rated_dishes, name='top_rated_dishes'),
]
