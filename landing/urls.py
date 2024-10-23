from django.shortcuts import redirect
from django.urls import path
from .views import *

app_name = 'landing'

urlpatterns = [
    path('landing', show_landing, name='landing'),
    path('create-suggestion-entry-ajax', add_suggestion_entry_ajax, name='add_suggestion_entry_ajax'),
]
