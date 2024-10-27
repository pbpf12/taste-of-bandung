from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from landing.models import Suggestion
from unittest.mock import patch
from django.http import HttpResponse

from django.test import TestCase
from django.contrib.auth.models import User
from main.models import Category, Restaurant, Suggestion, Dish, Review, ReviewVote, Bookmark, History


class RestaurantModelTest(TestCase):
    def setUp(self):
        # Create a sample restaurant for testing
        self.restaurant = Restaurant.objects.create(
            name="Sample Restaurant",
            address="123 Test St.",
            phone="123-456-7890",
            description="A test restaurant",
            average_rating=4.5,
            opening_hours="9:00 AM - 9:00 PM",
            image="https://example.com/image.jpg",
            price_range="$$"
        )

    def test_restaurant_creation(self):
        """Test restaurant model creation."""
        self.assertEqual(self.restaurant.name, "Sample Restaurant")
        self.assertEqual(self.restaurant.average_rating, 4.5)
        self.assertEqual(self.restaurant.price_range, "$$")


class SuggestionEntryTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.username = 'testuser'
        self.password = 'password'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client = Client()
        self.client.login(username=self.username, password=self.password)
        # Include the app name in the reverse call
        self.url = reverse('add_suggestion_entry_ajax')  # Use the namespace here

    def test_add_suggestion_success(self):
        response = self.client.post(self.url, {'suggestion': 'This is a test suggestion.'})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Suggestion.objects.count(), 1)
        self.assertEqual(Suggestion.objects.first().suggestionMessage, 'This is a test suggestion.')

    def test_add_suggestion_no_message(self):
        response = self.client.post(self.url, {'suggestion': ''})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Suggestion.objects.count(), 0)

    def test_add_suggestion_email_sent(self):
        response = self.client.post(self.url, {'suggestion': 'Another test suggestion.'})
        # Check if an email is sent or any other desired behavior here