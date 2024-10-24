from django.urls import path
from .views import last_activities_view, last_activities_page
from . import views

urlpatterns = [
    path('last-activities/', last_activities_view, name='last_activities'),  # AJAX view for fetching data
    path('last-activities-page/', last_activities_page, name='last_activities_page'),  # The page view
    path('delete_bookmark/', views.delete_bookmark, name='delete_bookmark'),
    path('delete_history/', views.delete_history, name='delete_history'),
]
