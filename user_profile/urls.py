from django.shortcuts import redirect
from django.urls import path
from .views import *

urlpatterns = [
    path('profile/<uuid:id>/', show_profile, name='profile'),
]
