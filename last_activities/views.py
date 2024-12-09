from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from main.models import Category, Restaurant, Suggestion, Dish, Review, ReviewVote, Bookmark, History
import json
from django.http import JsonResponse
from django.contrib.auth.models import AnonymousUser

@csrf_exempt
def last_activities_view(request):
    print(request.user)
    if isinstance(request.user, AnonymousUser):
        return JsonResponse({"error": "User not authenticated"}, status=401)
    
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
        }
        for bookmark in bookmarks
    ]

    return JsonResponse({'bookmarks': bookmark_list})

# View to render the HTML page
def last_activities_page(request):
    return render(request, 'last_activities_page.html')

# View to handle bookmark deletion
@csrf_exempt
@require_POST
def delete_bookmark(request):
    bookmark_id = request.POST.get('id')
    
    try:
        Bookmark.objects.get(id=bookmark_id).delete()
        return JsonResponse({'status': 'Bookmark deleted successfully'})
    except Bookmark.DoesNotExist:
        return JsonResponse({'status': 'Bookmark not found'}, status=404)

@csrf_exempt
def create_bookmark_flutter(request):
    if request.method == 'POST':
        try:
            # Parse incoming JSON data
            data = json.loads(request.body)

            # Check if the required fields are present
            user = request.user
            dish_id = data.get("dish_id")
            restaurant_id = data.get("restaurant_id")

            # Validate data
            if not (dish_id or restaurant_id):
                return JsonResponse({"status": "error", "message": "Dish ID or Restaurant ID must be provided"}, status=400)

            # Create or update the bookmark
            new_bookmark = Bookmark.objects.create(
                user=user,
                dish_id=dish_id if dish_id else None,
                restaurant_id=restaurant_id if restaurant_id else None,
            )
            new_bookmark.save()

            return JsonResponse({"status": "success", "bookmark_id": new_bookmark.id}, status=201)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)
