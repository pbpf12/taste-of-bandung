from django.urls import path
from . import views

urlpatterns = [
    path('dish/<int:dish_id>/', views.dish_detail, name='dish_detail'),
    path('dish/<int:dish_id>/bookmark/', views.bookmark_dish, name='bookmark_dish'),
    path('dish/<int:dish_id>/submit_review/', views.submit_review, name='submit_review'),
    path('review/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('review/<int:review_id>/vote/<str:vote_type>/', views.vote_review, name='vote_review'),
    path('restaurant/<int:restaurant_id>/', views.restaurant_detail, name='restaurant_detail'),
    path('review/check_limit/', views.check_review_limit, name='check_review_limit'),
]