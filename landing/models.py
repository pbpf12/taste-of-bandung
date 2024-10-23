from django.db import models

# Create your models here.
class Suggestion(models.Model):
    suggestionMessage = models.TextField()
