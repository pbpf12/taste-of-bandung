from django.urls import path
from . import views

urlpatterns = [
    path('last_activities/', views.last_activities_view, name='last_activities'),
    path('last_activities_page/', views.last_activities_page, name='last_activities_page'),
    path('delete_bookmark/', views.delete_bookmark, name='delete_bookmark'),
]