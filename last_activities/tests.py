from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Review, Bookmark, History, Dish, Restaurant

class LastActivitiesViewTest(TestCase):

    def setUp(self):
        # Create test users, dishes, restaurants, reviews, bookmarks, and histories
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.restaurant = Restaurant.objects.create(name='Test Restaurant', address='123 Test St', phone='123456789', description='A test restaurant', price_range='$$')
        self.dish = Dish.objects.create(name='Test Dish', restaurant=self.restaurant, category=None, price=10.00)
        
        Review.objects.create(user=self.user, dish=self.dish, rating=4, comment='Great dish!', restaurant=self.restaurant)
        Bookmark.objects.create(user=self.user, dish=self.dish)
        History.objects.create(user=self.user, dish=self.dish)

    def test_last_activities_view(self):
        # Simulate a request to the view
        response = self.client.get(reverse('last_activities'))

        # Check the response status and structure
        self.assertEqual(response.status_code, 200)
        self.assertIn('activities', response.json())

    def test_last_activities_page_view(self):
        # Test the page view that renders the template
        response = self.client.get(reverse('last_activities_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'last_activities_page.html')