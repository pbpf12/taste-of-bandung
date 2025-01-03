from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from main.models import Category, Restaurant, Suggestion, Dish, Review, ReviewVote, Bookmark, History


# View to load bookmarks (fetches real data from the database)
def last_activities_view(request):
    # Fetch bookmarks and related data
    bookmarks = Bookmark.objects.select_related('user', 'dish__restaurant').filter(user=request.user)

    # Create the list for JSON response, using `bookmark.dish.restaurant` if `bookmark.restaurant` is None
    bookmark_list = [
        {
            'id': bookmark.id,
            'user__username': bookmark.user.username,
            'restaurant__name': (
                bookmark.restaurant.name if bookmark.restaurant
                else (bookmark.dish.restaurant.name if bookmark.dish and bookmark.dish.restaurant else 'No Restaurant')
            ),
            'dish__name': bookmark.dish.name if bookmark.dish else 'No Dish Linked',
            'dish__id' : bookmark.dish.pk if bookmark.dish else 'No Dish Linked',
        }
        for bookmark in bookmarks
    ]

    return JsonResponse({'bookmarks': bookmark_list})

# View to render the HTML page
def last_activities_page(request):
    return render(request, 'last_activities_page.html')

@csrf_exempt
@require_POST
def delete_bookmark(request):
    bookmark_id = request.POST.get('id')

    try:
        # Retrieve the bookmark by ID
        bookmark = Bookmark.objects.get(id=bookmark_id)
        
        # Access the associated dish
        dish = bookmark.dish

        # Delete the bookmark
        bookmark.delete()

        # Update the bookmark count for the dish if it exists
        if dish is not None:
            dish.bookmark_count = max(0, dish.bookmark_count - 1)
            dish.save()

        return JsonResponse({'status': 'Bookmark deleted successfully'})
    except Bookmark.DoesNotExist:
        return JsonResponse({'status': 'Bookmark not found'}, status=404)
