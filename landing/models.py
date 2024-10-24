from django.db import models

# Create your models here.
class Suggestion(models.Model):
    suggestionMessage = models.TextField()

    def __str__(self):
        return self.suggestionMessage
