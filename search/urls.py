from django.urls import path
from .views import *

urlpatterns = [
    path('coba', coba, name="coba"),
    path('search', show_search_page, name="search"),
    path('get-dishes', get_dishes, name='get_dishes')
]
