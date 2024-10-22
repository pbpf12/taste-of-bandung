from django.db import models

# Create your models here.
class Restaurant(models.Model):
    name = models.CharField(max_length=100)

class Dish(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.IntegerField()
    image_url = models.TextField()
