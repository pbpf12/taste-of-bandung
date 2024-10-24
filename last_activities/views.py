from django.shortcuts import render
from .models import Review, Bookmark, History  # Import the models
from django.http import JsonResponse

from django.http import JsonResponse
from main.management.seeds.contoh import bookmarks_contoh, history_contoh  # Import dummy data

def last_activities_view(request):
    # Use the dummy data for bookmarks and history
    bookmarks = bookmarks_contoh
    history = history_contoh

    # Return the data as JSON response
    return JsonResponse({
        'bookmarks': bookmarks,
        'history': history,
    })

def last_activities_page(request):
    return render(request, 'last_activities_page.html')

def delete_bookmark(request):
    if request.method == 'POST':
        bookmark_id = request.POST.get('id')
        Bookmark.objects.filter(id=bookmark_id).delete()
        return JsonResponse({'status': 'Bookmark deleted successfully'})

def delete_history(request):
    if request.method == 'POST':
        history_id = request.POST.get('id')
        History.objects.filter(id=history_id).delete()
        return JsonResponse({'status': 'History deleted successfully'})
