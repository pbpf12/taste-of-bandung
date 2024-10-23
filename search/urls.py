from django.urls import path
from .views import *

urlpatterns = [
    path('search', show_search_page, name="search"),
    path('get-dishes', get_dishes, name='get_dishes'),
    path('get-all-dishes', get_all_dishes, name="get_all_dishes"),
]