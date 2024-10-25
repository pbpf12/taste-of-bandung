from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login
import datetime
from django.http import HttpResponseRedirect


# Create your views here.
def check_authentication(request):
    if request.COOKIES == None:
        return redirect('login')
    
    response = HttpResponseRedirect(reverse('landing'))
    response.set_cookie('last_login', str(datetime.datetime.now()))
    return response

def login_user(request):
    next_url = (request.GET.get('next', '/')).replace('-', '_').replace('/','')

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse(next_url))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response
        else:
            messages.error(request, "Invalid username or password. Please try again.")

    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)
