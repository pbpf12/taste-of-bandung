from django.urls import path
from .views import *

# kalau bisa, samain nama routing render pagenya kyak nama appnya, biar gampang routingnya
urlpatterns = [
    path('main1', main1, name='main1'), # <== kyak gini
    path('main2', main2, name='main2'),
    path('logout/', logout_user, name='logout')  # <== logout taro di navbar aja gasihhh
]
