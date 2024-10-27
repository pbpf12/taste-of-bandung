from django.contrib import admin
from main.models import Review, ReviewVote

# Register your models here.
admin.site.register(Review)
admin.site.register(ReviewVote)