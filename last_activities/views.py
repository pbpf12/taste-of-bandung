from django.shortcuts import render
from .models import Review, Bookmark, History  # Import the models
from django.http import JsonResponse

def last_activities_view(request):
    # Query the most recent reviews, bookmarks, and history records
    recent_reviews = Review.objects.order_by('-created_at')[:5]  # Latest 5 reviews
    recent_bookmarks = Bookmark.objects.order_by('-created_at')[:5]  # Latest 5 bookmarks
    recent_histories = History.objects.order_by('-created_at')[:5]  # Latest 5 history records

    # Combine and format the data into a list of activities
    activities = []

    for review in recent_reviews:
        activities.append({
            'type': 'Review',
            'user': review.user.username,
            'content': f'Reviewed {review.dish.name}' if review.dish else f'Reviewed {review.restaurant.name}',
            'created_at': review.created_at,
        })

    for bookmark in recent_bookmarks:
        activities.append({
            'type': 'Bookmark',
            'user': bookmark.user.username,
            'content': f'Bookmarked {bookmark.dish.name}' if bookmark.dish else f'Bookmarked {bookmark.restaurant.name}',
            'created_at': bookmark.created_at,
        })

    for history in recent_histories:
        activities.append({
            'type': 'History',
            'user': history.user.username,
            'content': f'Viewed {history.dish.name}',
            'created_at': history.created_at,
        })

    # Sort all activities by the `created_at` field in descending order
    sorted_activities = sorted(activities, key=lambda x: x['created_at'], reverse=True)

    return JsonResponse({'activities': sorted_activities})

def last_activities_page(request):
    return render(request, 'last_activities_page.html')
