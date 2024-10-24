from django.urls import path
from .views import *

urlpatterns = [
    path('search', show_search_page, name="search"),
    path('get-dishes', get_dishes, name='get_dishes'),
]