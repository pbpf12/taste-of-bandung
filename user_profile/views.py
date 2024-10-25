from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils.html import strip_tags
from main.models import History


@login_required
def show_json(request):
    user = request.user
    return JsonResponse({
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
    })

def show_profile(request):
    user = request.user
    
    # Check if the profile is incomplete
    if not user.first_name or not user.last_name or not user.email:
        messages.warning(request, "Your profile is incomplete. Please update your details.")
    

    
    return render(request, "profile.html")

def delete_user(request):
    user = request.user

    user.delete()
    messages.success(request, "Your account has been deleted.")

    return redirect(reverse('login'))

@csrf_exempt
@require_POST
def edit_profile(request):
    if request.method == 'POST':
        try:
            user = request.user
            user.first_name = strip_tags(request.POST.get('first_name', user.first_name))
            user.last_name = strip_tags(request.POST.get('last_name', user.last_name))
            user.email = request.POST.get('email', user.email)
            user.save()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Profile updated successfully',
                'user': {
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'username': user.username,
                }
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def show_history_as_json(request):
    user = request.user
    history = History.objects.filter(user=user).order_by('-created_at')

    return JsonResponse({
        'history': [
            {
                'dish': {
                    'name': h.dish.name,
                    'restaurant': h.dish.restaurant.name,
                    'price': h.dish.price,
                    'image': h.dish.image,
                },
                'created_at': h.created_at,
            }
            for h in history
        ]
    })

def clear_history(request):
    user = request.user
    History.objects.filter(user=user).delete()

    return redirect(reverse('show_history'))