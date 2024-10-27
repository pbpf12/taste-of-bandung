from django.db import models
from django.contrib.auth.models import User
from main.models import Restaurant,  Dish


# Bookmark Model
class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True, blank=True)
    dish = models.ForeignKey(Dish, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bookmark by {self.user.username}"