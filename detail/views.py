from django.shortcuts import render

# Create your views here.
def show_detail(request):
    return render(request, 'detail_page.html')
