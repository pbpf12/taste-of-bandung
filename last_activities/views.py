from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from main.models import Bookmark

# View to load bookmarks (fetches real data from the database)
def last_activities_view(request):
    # Fetch all bookmarks and select related user, restaurant, and dish
    bookmarks = Bookmark.objects.select_related('user', 'restaurant', 'dish').all()

    # Prepare data to be sent as JSON
    bookmark_list = [
        {
            'id': bookmark.id,
            'user__username': bookmark.user.username,
            'restaurant__name': bookmark.restaurant.name if bookmark.restaurant else '',
            'dish__name': bookmark.dish.name if bookmark.dish else '',
        }
        for bookmark in bookmarks
    ]

    # Return data as JSON
    return JsonResponse({
        'bookmarks': bookmark_list,
    })

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
