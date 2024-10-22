from django.shortcuts import redirect
from django.urls import path
from .views import *

urlpatterns = [
    path('', landing, name='landing'),
]
