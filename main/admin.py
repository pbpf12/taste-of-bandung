from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Restaurant)
admin.site.register(Category)
admin.site.register(Dish)
admin.site.register(Review)
admin.site.register(Bookmark)
admin.site.register(History)