from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from main.models import Category, Restaurant, Suggestion, Dish, Review, ReviewVote, Bookmark, History


User = get_user_model()

class DishDetailViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        self.category = Category.objects.create(name="Main Course")
        self.restaurant = Restaurant.objects.create(
            name="Test Restaurant",
            address="123 Test Street",
            phone="123456789",
            description="A test restaurant.",
            image="http://test.com/image.jpg",
            price_range="$$",
        )
        self.dish = Dish.objects.create(
            name="Test Dish",
            description="A test dish",
            price=10000,
            image="http://test.com/dish.jpg",
            restaurant=self.restaurant,
            category=self.category
        )

    def test_dish_detail_view(self):
        response = self.client.get(reverse('dish_detail', args=[self.dish.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.dish.name)
        self.assertContains(response, "Rp.10000")

    def test_submit_review(self):
        response = self.client.post(
            reverse('submit_review', args=[self.dish.id]),
            data={'rating': 4, 'comment': "Great dish!"},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Review.objects.filter(dish=self.dish, user=self.user).exists())

    def test_edit_review(self):
        review = Review.objects.create(dish=self.dish, user=self.user, rating=4, comment="Good dish!")
        response = self.client.post(
            reverse('edit_review', args=[review.id]),
            data={'rating': 5, 'comment': "Excellent dish!"},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        review.refresh_from_db()
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "Excellent dish!")

    def test_delete_review(self):
        review = Review.objects.create(dish=self.dish, user=self.user, rating=4, comment="Good dish!")
        response = self.client.post(reverse('delete_review', args=[review.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Review.objects.filter(id=review.id).exists())

    def test_toggle_bookmark(self):
        response = self.client.post(reverse('bookmark_dish', args=[self.dish.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Bookmark.objects.filter(dish=self.dish, user=self.user).exists())

        response = self.client.post(reverse('bookmark_dish', args=[self.dish.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Bookmark.objects.filter(dish=self.dish, user=self.user).exists())

    def test_upvote_review(self):
        review = Review.objects.create(dish=self.dish, user=self.user, rating=4, comment="Nice!")
        response = self.client.post(reverse('vote_review', args=[review.id, 'upvote']), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ReviewVote.objects.filter(review=review, user=self.user, vote_type=ReviewVote.UPVOTE).exists())

    def test_downvote_review(self):
        review = Review.objects.create(dish=self.dish, user=self.user, rating=4, comment="Nice!")
        response = self.client.post(reverse('vote_review', args=[review.id, 'downvote']), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(ReviewVote.objects.filter(review=review, user=self.user, vote_type=ReviewVote.DOWNVOTE).exists())

    def test_create_history_entry(self):
        response = self.client.get(reverse('dish_detail', args=[self.dish.id]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(History.objects.filter(dish=self.dish, user=self.user).exists())
