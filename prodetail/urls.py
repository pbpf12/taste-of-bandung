from django.urls import path
from .views import *

urlpatterns = [
    path('prodetail', prodetail, name='prodetail'),
]
