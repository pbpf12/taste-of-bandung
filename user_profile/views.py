from django.shortcuts import render, redirect
from main.models import User
from .forms import UserForm

def show_profile(request):
    return render(request, "profile.html")
