from django.contrib import admin
from main.models import Category, Restaurant, Suggestion

# Register your models here.
admin.site.register(Category)
admin.site.register(Restaurant)
admin.site.register(Suggestion)