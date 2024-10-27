from django.urls import path
from .views import *

urlpatterns = [
    path('', check_authentication, name=''), 
    path('login/', login_user, name='login'), 
]
