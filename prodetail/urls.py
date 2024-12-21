from django.urls import path
from . import views

urlpatterns = [
    # Existing Web URL patterns
    path('dish/<int:dish_id>/', views.dish_detail, name='dish_detail'),
    path('dish/<int:dish_id>/bookmark/', views.bookmark_dish, name='bookmark_dish'),
    path('dish/<int:dish_id>/submit_review/', views.submit_review, name='submit_review'),
    path('review/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('review/<int:review_id>/delete/', views.delete_review, name='delete_review'),
    path('review/<int:review_id>/vote/<str:vote_type>/', views.vote_review, name='vote_review'),
    path('restaurant/<int:restaurant_id>/', views.restaurant_detail, name='restaurant_detail'),
    path('review/check_limit/', views.check_review_limit, name='check_review_limit'),

    # API URL patterns
    path('api/dishes/<int:dish_id>/', views.dish_detail_api, name='dish_detail_api'),
    path('api/dishes/<int:dish_id>/bookmark/', views.bookmark_dish_api, name='bookmark_dish_api'),
    # Add the following line to handle POST to /api/dishes/<dish_id>/reviews/
    path('api/dishes/<int:dish_id>/reviews/', views.submit_review_api, name='submit_review_api'),
    path('api/reviews/<int:review_id>/edit/', views.edit_review_api, name='edit_review_api'),
    path('api/reviews/<int:review_id>/delete/', views.delete_review_api, name='delete_review_api'),
    path('api/reviews/<int:review_id>/vote/<str:vote_type>/', views.vote_review_api, name='vote_review_api'),
    path('api/restaurants/<int:restaurant_id>/', views.restaurant_detail_api, name='restaurant_detail_api'),
    path('api/reviews/check_limit/', views.check_review_limit_api, name='check_review_limit_api'),
]
