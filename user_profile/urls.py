from django.shortcuts import redirect
from django.urls import path
from .views import *

urlpatterns = [
    path('profile/', show_profile, name='profile'),
    path('delete/', delete_user, name='delete_user'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('show_json/', show_json, name='show_json'),
    path('show_history/', show_history_as_json, name='show_history'),
    path('clear_history/', clear_history, name='clear_history'),
    path('edit_profile_flutter/', edit_profile_flutter, name='edit_profile_flutter'),
]
