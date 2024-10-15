from django.shortcuts import render, redirect

def show_profile(request):
    return render(request, "profile.html")
