from django.db import models
from django.contrib.auth.models import User
from main.models import Restaurant,Dish


# Create your models here.
# Review Model
class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True, blank=True)
    dish = models.ForeignKey(Dish, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # Rating from 1 to 5
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"{self.user.username} - {self.rating}"
    
# Vote Model for Review
class ReviewVote(models.Model):
    UPVOTE = 1
    DOWNVOTE = -1
    VOTE_CHOICES = [
        (UPVOTE, 'Upvote'),
        (DOWNVOTE, 'Downvote')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    vote_type = models.IntegerField(choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'review')  # Ensure a user can vote once per review

    def str(self):
        vote_str = "Upvote" if self.vote_type == self.UPVOTE else "Downvote"
        return f"{self.user.username} {vote_str} on review {self.review.id}"