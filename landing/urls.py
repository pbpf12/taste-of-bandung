from django.shortcuts import redirect
from django.urls import path
from .views import *
from django.urls import path, include 

urlpatterns = [
    path('landing', show_landing, name='landing'),
    path('create-suggestion-entry-ajax', add_suggestion_entry_ajax, name='add_suggestion_entry_ajax'),
    path('top-rated-dishes/', top_rated_dishes, name='top_rated_dishes'),
    # path('landing/json', show_landing_json, name='landing_json'),  # JSON view
    path('landing/json/', show_json_dishes, name='show_json'),
    path('landing/json-suggestion/', show_json_suggestions, name='show_json_suggestion'),
     path('landing/create-suggestion-flutter/', create_suggestion_flutter, name='create_suggestion_flutter'),
]
