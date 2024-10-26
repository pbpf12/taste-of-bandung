from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from main.models import Dish, Review, Bookmark, Restaurant, History, ReviewVote
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now, timedelta
from django.db.models import Avg
from django.views.decorators.http import require_POST
from django.utils import timezone

def update_dish_history(user, dish):
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
    dish = get_object_or_404(Dish, id=dish_id)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, dish=dish)
    
    if not created:
        bookmark.delete()
        dish.bookmark_count = max(0, dish.bookmark_count - 1)
        message = 'Bookmark removed'
    else:
        dish.bookmark_count += 1
        message = 'Bookmarked'
        
    dish.save()
    
    return JsonResponse({
        'message': message,
        'bookmark_count': dish.bookmark_count
    })

@login_required
@require_POST
def submit_review(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    rating = request.POST.get('rating')
    comment = request.POST.get('comment')

    if not rating or not comment:
        return JsonResponse({'error': 'Rating and comment are required.'}, status=400)

    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            return JsonResponse({'error': 'Rating must be between 1 and 5.'}, status=400)
    except ValueError:
        return JsonResponse({'error': 'Invalid rating format.'}, status=400)

    review = Review.objects.create(user=request.user, dish=dish, rating=rating, comment=comment)
    
    average_rating = Review.objects.filter(dish=dish).aggregate(Avg('rating'))['rating__avg']
    dish.average_rating = average_rating
    dish.save()

    return JsonResponse({
        'message': 'Review submitted successfully!',
        'average_rating': average_rating,
        'new_review_id': review.id
    })

@login_required
def check_review_limit(request):
    last_24_hours = now() - timedelta(days=1)
    review_count = Review.objects.filter(user=request.user, created_at__gte=last_24_hours).count()
    limit_reached = review_count >= 5
    reviews_remaining = 5 - review_count if review_count < 5 else 0
    
    return JsonResponse({
        'limit_reached': limit_reached,
        'reviews_remaining': reviews_remaining,
        'review_count': review_count
    })

@login_required
@require_POST
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    rating = request.POST.get('rating')
    comment = request.POST.get('comment')

    if rating:
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                return JsonResponse({'error': 'Rating must be between 1 and 5'}, status=400)
        except ValueError:
            return JsonResponse({'error': 'Invalid rating format'}, status=400)

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
            'message': 'Review updated successfully!',
            'average_rating': average_rating
        })

    return JsonResponse({'error': 'No valid data provided for update'}, status=400)

@login_required
@require_POST
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    dish = review.dish
    review.delete()

    average_rating = Review.objects.filter(dish=dish).aggregate(Avg('rating'))['rating__avg']
    if average_rating is None: 
        average_rating = 0
    
    dish.average_rating = average_rating
    dish.save()

    return JsonResponse({
        'message': 'Review deleted successfully!',
        'average_rating': average_rating
    })

@login_required
@require_POST
def vote_review(request, review_id, vote_type):
    review = get_object_or_404(Review, id=review_id)
    user = request.user

    existing_vote = ReviewVote.objects.filter(user=user, review=review).first()

    if vote_type == 'upvote':
        if existing_vote and existing_vote.vote_type == 1:
            existing_vote.delete()
        else:
            ReviewVote.objects.update_or_create(user=user, review=review, defaults={'vote_type': 1})
    elif vote_type == 'downvote':
        if existing_vote and existing_vote.vote_type == -1:
            existing_vote.delete() 
        else:
            ReviewVote.objects.update_or_create(user=user, review=review, defaults={'vote_type': -1})

    upvotes = ReviewVote.objects.filter(review=review, vote_type=1).count()
    downvotes = ReviewVote.objects.filter(review=review, vote_type=-1).count()

    return JsonResponse({
        'upvotes': upvotes,
        'downvotes': downvotes,
        'total_votes': upvotes + downvotes
    })

def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    
    response_data = {
        'name': restaurant.name,
        'description': restaurant.description,
        'address': restaurant.address,
        'phone': restaurant.phone,
        'opening_hours': restaurant.opening_hours,
        'image': restaurant.image,
        'price_range': restaurant.price_range
    }
    
    return JsonResponse(response_data)
