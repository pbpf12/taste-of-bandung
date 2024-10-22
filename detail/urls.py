from django.urls import path
from .views import *

urlpatterns = [
    path('detail', show_detail, name='detail'), 

]
