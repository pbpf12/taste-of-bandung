# lib/features/prodetail/views.py

import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from main.models import Category, Restaurant, Suggestion, Dish, Review, ReviewVote, Bookmark, History
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now, timedelta
from django.db.models import Avg
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt  # Import csrf_exempt
from django.views.decorators.http import require_http_methods

# ---------------- Helper Functions ----------------

def update_dish_history(user, dish):
    """Helper function to update user's dish history"""
    existing_history = History.objects.filter(user=user, dish=dish).first()
    
    if existing_history:
        existing_history.created_at = timezone.now()
        existing_history.save()
    else:
        History.objects.create(user=user, dish=dish)
        
        history_count = History.objects.filter(user=user).count()

        if history_count > 5:
            recent_ids = History.objects.filter(user=user).order_by('-created_at')[:5].values_list('id', flat=True)
            History.objects.filter(user=user).exclude(id__in=list(recent_ids)).delete()

# ---------------- Web Views ----------------

def dish_detail(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    update_dish_history(request.user, dish)
    is_bookmarked = Bookmark.objects.filter(user=request.user, dish=dish).exists()
    dish.is_bookmarked = is_bookmarked

    reviews = Review.objects.filter(dish=dish).annotate(
        vote_score=Avg('reviewvote__vote_type')
    ).order_by(
        '-vote_score', '-created_at'
    )

    # Put the current user's reviews at the top
    if request.user.is_authenticated:
        user_reviews = reviews.filter(user=request.user)
        other_reviews = reviews.exclude(user=request.user)
        reviews = list(user_reviews) + list(other_reviews)
    else:
        reviews = list(reviews)

    review_data = [{
        'id': review.id,
        'user': review.user.username,
        'rating': review.rating,
        'comment': review.comment,
        'upvotes': ReviewVote.objects.filter(review=review, vote_type=1).count(),
        'downvotes': ReviewVote.objects.filter(review=review, vote_type=-1).count(),
        'is_author': review.user == request.user 
    } for review in reviews]
    
    rating_avg = dish.average_rating or "No rating yet"

    context = {
        'dish': dish,
        'reviews': review_data,
        'restaurant': dish.restaurant,
        'rating_avg': rating_avg,
    }

    return render(request, 'dish_detail.html', context)


@login_required
@require_POST
def bookmark_dish(request, dish_id):
    try:
        dish = get_object_or_404(Dish, id=dish_id)
        bookmark, created = Bookmark.objects.get_or_create(user=request.user, dish=dish)
        
        if not created:
            bookmark.delete()
            dish.bookmark_count = max(0, dish.bookmark_count - 1)
            message = 'Bookmark removed'
            is_bookmarked = False
        else:
            dish.bookmark_count += 1
            message = 'Bookmarked'
            is_bookmarked = True
            
        dish.save()
        
        return JsonResponse({
            'status': 'success',
            'message': message,
            'bookmark_count': dish.bookmark_count,
            'is_bookmarked': is_bookmarked
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
@require_POST
def submit_review(request, dish_id):
    try:
        dish = get_object_or_404(Dish, id=dish_id)
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if not rating or not comment:
            return JsonResponse({'status': 'error', 'message': 'Rating and comment are required.'}, status=400)

        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                return JsonResponse({'status': 'error', 'message': 'Rating must be between 1 and 5.'}, status=400)
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid rating format.'}, status=400)

        review = Review.objects.create(user=request.user, dish=dish, rating=rating, comment=comment)
        
        average_rating = Review.objects.filter(dish=dish).aggregate(Avg('rating'))['rating__avg']
        dish.average_rating = average_rating
        dish.save()

        return JsonResponse({
            'status': 'success',
            'message': 'Review submitted successfully!',
            'average_rating': average_rating,
            'new_review_id': review.id
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
def check_review_limit(request):
    try:
        last_24_hours = now() - timedelta(days=1)
        review_count = Review.objects.filter(user=request.user, created_at__gte=last_24_hours).count()
        limit_reached = review_count >= 5
        reviews_remaining = 5 - review_count if review_count < 5 else 0
        
        return JsonResponse({
            'status': 'success',
            'limit_reached': limit_reached,
            'reviews_remaining': reviews_remaining,
            'review_count': review_count
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
@require_POST
def edit_review(request, review_id):
    try:
        review = get_object_or_404(Review, id=review_id, user=request.user)
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if rating:
            try:
                rating = int(rating)
                if rating < 1 or rating > 5:
                    return JsonResponse({'status': 'error', 'message': 'Rating must be between 1 and 5'}, status=400)
            except ValueError:
                return JsonResponse({'status': 'error', 'message': 'Invalid rating format'}, status=400)

        if comment or rating:
            if rating:
                review.rating = rating
            if comment:
                review.comment = comment

            review.save()

            dish = review.dish
            average_rating = Review.objects.filter(dish=dish).aggregate(Avg('rating'))['rating__avg'] or 0
            dish.average_rating = average_rating
            dish.save()

            return JsonResponse({
                'status': 'success',
                'message': 'Review updated successfully!',
                'average_rating': average_rating
            })
        
        return JsonResponse({'status': 'error', 'message': 'No valid data provided for update'}, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
@require_POST
def delete_review(request, review_id):
    try:
        review = get_object_or_404(Review, id=review_id, user=request.user)
        dish = review.dish
        review.delete()

        average_rating = Review.objects.filter(dish=dish).aggregate(Avg('rating'))['rating__avg']
        if average_rating is None: 
            average_rating = 0
        
        dish.average_rating = average_rating
        dish.save()

        return JsonResponse({
            'status': 'success',
            'message': 'Review deleted successfully!',
            'average_rating': average_rating
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
@require_POST
def vote_review(request, review_id, vote_type):
    try:
        review = get_object_or_404(Review, id=review_id)
        user = request.user

        existing_vote = ReviewVote.objects.filter(user=user, review=review).first()

        if vote_type == 'upvote':
            if existing_vote and existing_vote.vote_type == 1:
                existing_vote.delete()
                message = 'Upvote removed'
            else:
                ReviewVote.objects.update_or_create(user=user, review=review, defaults={'vote_type': 1})
                message = 'Upvoted'
        elif vote_type == 'downvote':
            if existing_vote and existing_vote.vote_type == -1:
                existing_vote.delete() 
                message = 'Downvote removed'
            else:
                ReviewVote.objects.update_or_create(user=user, review=review, defaults={'vote_type': -1})
                message = 'Downvoted'
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid vote type.'}, status=400)

        upvotes = ReviewVote.objects.filter(review=review, vote_type=1).count()
        downvotes = ReviewVote.objects.filter(review=review, vote_type=-1).count()

        return JsonResponse({
            'status': 'success',
            'message': message,
            'upvotes': upvotes,
            'downvotes': downvotes,
            'total_votes': upvotes + downvotes
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

def restaurant_detail(request, restaurant_id):
    try:
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        
        response_data = {
            'name': restaurant.name,
            'description': restaurant.description,
            'address': restaurant.address,
            'phone': restaurant.phone,
            'opening_hours': restaurant.opening_hours,
            'image': restaurant.image if restaurant.image else None,  # Assuming image is a FileField/ImageField
            'price_range': restaurant.price_range
        }
        
        return JsonResponse({
            'status': 'success',
            'restaurant': response_data
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

#----------------------------------

# ---------------- API Views ----------------

@csrf_exempt
@login_required
@require_http_methods(["GET"])
def dish_detail_api(request, dish_id):
    """API endpoint for dish details"""
    try:
        dish = get_object_or_404(Dish, id=dish_id)
        
        # Update dish history if user is authenticated
        if request.user.is_authenticated:
            update_dish_history(request.user, dish)
        
        # Check if dish is bookmarked
        is_bookmarked = Bookmark.objects.filter(user=request.user, dish=dish).exists() if request.user.is_authenticated else False

        # Retrieve reviews with vote scores
        reviews = Review.objects.filter(dish=dish).annotate(
            vote_score=Avg('reviewvote__vote_type')
        ).order_by('-vote_score', '-created_at')

        # Prepare review data
        review_data = [{
            'id': review.id,
            'user': review.user.username,
            'rating': review.rating,
            'comment': review.comment,
            'upvotes': ReviewVote.objects.filter(review=review, vote_type=1).count(),
            'downvotes': ReviewVote.objects.filter(review=review, vote_type=-1).count(),
            'is_author': request.user.is_authenticated and review.user == request.user 
        } for review in reviews]
        
        # Prepare dish data
        dish_data = {
            'id': dish.id,
            'name': dish.name,
            'description': dish.description,
            'price': str(dish.price),  # Convert to string to ensure JSON serialization
            'category': dish.category.name if dish.category else None,
            'restaurant_id': dish.restaurant.id,
            'restaurant_name': dish.restaurant.name,
            'average_rating': dish.average_rating or 0,
            'bookmark_count': dish.bookmark_count,
            'is_bookmarked': is_bookmarked,
            'image': dish.image if dish.image else None  # Assuming image is a FileField/ImageField
        }

        return JsonResponse({
            'status': 'success',
            'dish': dish_data,
            'reviews': review_data
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@csrf_exempt  # Exempt from CSRF protection
@login_required
@require_POST
def bookmark_dish_api(request, dish_id):
    """API endpoint for bookmarking/unbookmarking a dish"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
    
    try:
        dish = get_object_or_404(Dish, id=dish_id)
        
        bookmark, created = Bookmark.objects.get_or_create(user=request.user, dish=dish)
        
        if not created:
            bookmark.delete()
            dish.bookmark_count = max(0, dish.bookmark_count - 1)
            message = 'Bookmark removed'
            is_bookmarked = False
        else:
            dish.bookmark_count += 1
            message = 'Bookmarked'
            is_bookmarked = True
            
        dish.save()
        
        return JsonResponse({
            'status': 'success',
            'message': message,
            'bookmark_count': dish.bookmark_count,
            'is_bookmarked': is_bookmarked
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)
    
@csrf_exempt
@login_required
@require_POST
def submit_review_api(request, dish_id):
    """API endpoint for submitting a review"""
    try:
        dish = get_object_or_404(Dish, id=dish_id)
        
        # Get data from POST parameters
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if not rating or not comment:
            return JsonResponse({
                'status': 'error', 
                'message': 'Rating and comment are required.'
            }, status=400)

        try:
            rating = int(rating)
            if not (1 <= rating <= 5):
                return JsonResponse({
                    'status': 'error',
                    'message': 'Rating must be between 1 and 5'
                }, status=400)
        except ValueError:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid rating format'
            }, status=400)

        # Create review
        review = Review.objects.create(
            user=request.user,
            dish=dish,
            rating=rating,
            comment=comment
        )
        
        # Update dish average rating
        average_rating = Review.objects.filter(dish=dish).aggregate(Avg('rating'))['rating__avg']
        dish.average_rating = average_rating
        dish.save()

        # Return review data in response
        return JsonResponse({
            'status': 'success',
            'message': 'Review submitted successfully!',
            'review': {
                'id': review.id,
                'user': review.user.username,
                'rating': review.rating,
                'comment': review.comment,
                'upvotes': 0,
                'downvotes': 0,
                'is_author': True
            }
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)
    
@csrf_exempt
@login_required
@require_POST
def edit_review_api(request, review_id):
    """API endpoint for editing a review"""
    try:
        review = get_object_or_404(Review, id=review_id, user=request.user)
        
        # Try to get data from both POST and body
        try:
            data = json.loads(request.body)
            rating = data.get('rating')
            comment = data.get('comment')
        except:
            rating = request.POST.get('rating')
            comment = request.POST.get('comment')

        if not rating and not comment:
            return JsonResponse({
                'status': 'error',
                'message': 'No data provided for update'
            }, status=400)

        if rating:
            try:
                rating = int(rating)
                if not (1 <= rating <= 5):
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Rating must be between 1 and 5'
                    }, status=400)
                review.rating = rating
            except ValueError:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid rating format'
                }, status=400)

        if comment:
            review.comment = comment

        review.save()

        # Update dish average rating
        dish = review.dish
        average_rating = Review.objects.filter(dish=dish).aggregate(Avg('rating'))['rating__avg'] or 0
        dish.average_rating = average_rating
        dish.save()

        return JsonResponse({
            'status': 'success',
            'message': 'Review updated successfully!',
            'review': {
                'id': review.id,
                'user': review.user.username,
                'rating': review.rating,
                'comment': review.comment,
                'upvotes': ReviewVote.objects.filter(review=review, vote_type=1).count(),
                'downvotes': ReviewVote.objects.filter(review=review, vote_type=-1).count(),
                'is_author': True
            }
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@csrf_exempt  # Exempt from CSRF protection
@login_required
@require_POST
def delete_review_api(request, review_id):
    """API endpoint for deleting a review"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
    
    try:
        review = get_object_or_404(Review, id=review_id, user=request.user)
        dish = review.dish
        review.delete()

        # Recalculate dish average rating
        average_rating = Review.objects.filter(dish=dish).aggregate(Avg('rating'))['rating__avg']
        average_rating = average_rating or 0
        
        dish.average_rating = average_rating
        dish.save()

        return JsonResponse({
            'status': 'success',
            'message': 'Review deleted successfully!',
            'average_rating': average_rating
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@csrf_exempt  # Exempt from CSRF protection
@login_required
@require_POST
def vote_review_api(request, review_id, vote_type):
    """API endpoint for voting on a review"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
    
    try:
        review = get_object_or_404(Review, id=review_id)
        user = request.user

        existing_vote = ReviewVote.objects.filter(user=user, review=review).first()

        if vote_type == 'upvote':
            if existing_vote and existing_vote.vote_type == 1:
                existing_vote.delete()
                message = 'Upvote removed'
            else:
                ReviewVote.objects.update_or_create(user=user, review=review, defaults={'vote_type': 1})
                message = 'Upvoted'
        elif vote_type == 'downvote':
            if existing_vote and existing_vote.vote_type == -1:
                existing_vote.delete() 
                message = 'Downvote removed'
            else:
                ReviewVote.objects.update_or_create(user=user, review=review, defaults={'vote_type': -1})
                message = 'Downvoted'
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid vote type.'}, status=400)

        upvotes = ReviewVote.objects.filter(review=review, vote_type=1).count()
        downvotes = ReviewVote.objects.filter(review=review, vote_type=-1).count()

        return JsonResponse({
            'status': 'success',
            'message': message,
            'upvotes': upvotes,
            'downvotes': downvotes,
            'total_votes': upvotes + downvotes
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@csrf_exempt
@login_required
@require_http_methods(["GET"])
def restaurant_detail_api(request, restaurant_id):
    """API endpoint for restaurant details"""
    if request.method != 'POST' and request.method != 'GET':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
    
    try:
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)
        
        # Get dishes for the restaurant
        dishes = Dish.objects.filter(restaurant=restaurant).values(
            'id', 'name', 'description', 'price', 'average_rating', 'image'
        )

        # Process image URLs
        dishes = list(dishes)
        for dish in dishes:
            if dish['image']:
                dish['image'] = dish['image']
            else:
                dish['image'] = None  # Or provide a default image URL

        restaurant_data = {
            'id': restaurant.id,
            'name': restaurant.name,
            'description': restaurant.description,
            'address': restaurant.address,
            'phone': restaurant.phone,
            'opening_hours': restaurant.opening_hours,
            'image': restaurant.image if restaurant.image else None,  # Assuming image is a FileField/ImageField
            'price_range': restaurant.price_range
        }

        return JsonResponse({
            'status': 'success',
            'restaurant': restaurant_data,
            'dishes': dishes
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@csrf_exempt  # Exempt from CSRF protection
@login_required
@require_POST
def check_review_limit_api(request):
    """API endpoint to check review submission limit"""
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Method not allowed'}, status=405)
    
    try:
        last_24_hours = now() - timedelta(days=1)
        review_count = Review.objects.filter(user=request.user, created_at__gte=last_24_hours).count()
        limit_reached = review_count >= 5
        reviews_remaining = 5 - review_count if review_count < 5 else 0
        

        return JsonResponse({
            'status': 'success',
            'limit_reached': limit_reached,
            'reviews_remaining': reviews_remaining,
            'review_count': review_count
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)