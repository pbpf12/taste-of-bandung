from django.db import models
from main.models import User

# Create your models here.
class Suggestion(models.Model):
    suggestionMessage = models.TextField()

    def __str__(self):
        return self.suggestionMessage
