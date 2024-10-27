from django.db import models
from django.contrib.auth.models import User
from main.models import  Dish


# Create your models here.
# History Model
class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"History for {self.user.username}"
    