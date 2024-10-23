from django.urls import path
from .views import last_activities_view, last_activities_page

urlpatterns = [
    path('last-activities/', last_activities_view, name='last_activities'),  # AJAX view for fetching data
    path('last-activities-page/', last_activities_page, name='last_activities_page'),  # The page view
]
