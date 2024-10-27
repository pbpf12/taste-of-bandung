from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=15)
    description = models.TextField()
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    opening_hours = models.CharField(max_length=100, null=True, blank=True)
    image = models.URLField()
    price_range = models.CharField(max_length=100)

class Suggestion(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    suggestionMessage = models.TextField()

    def __str__(self):
        return self.suggestionMessage