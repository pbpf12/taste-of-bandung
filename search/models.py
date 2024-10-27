from django.db import models
from django.contrib.auth.models import User
from main.models import Category, Restaurant


# Update Dish Model
class Dish(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.URLField()
    bookmark_count = models.IntegerField(default=0)