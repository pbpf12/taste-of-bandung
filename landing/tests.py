from django.test import TestCase

# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from landing.models import Suggestion
from main.models import Dish, Restaurant
from unittest.mock import patch
from django.http import HttpResponse

from django.test import TestCase
from django.contrib.auth.models import User
from .models import Restaurant, Dish, Review, Category

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

    def test_restaurant_string_representation(self):
        """Test the string representation of the Restaurant model."""
        self.assertEqual(str(self.restaurant), "Sample Restaurant")


class DishModelTest(TestCase):
    def setUp(self):
        # Create a sample category and restaurant for the dish
        self.category = Category.objects.create(name="Main Course")
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
        # Create a sample dish for testing
        self.dish = Dish.objects.create(
            restaurant=self.restaurant,
            category=self.category,
            name="Sample Dish",
            description="A test dish",
            average_rating=4.2,
            price=12.99,
            image="https://example.com/dish.jpg",
            bookmark_count=10
        )

    def test_dish_creation(self):
        """Test dish model creation."""
        self.assertEqual(self.dish.name, "Sample Dish")
        self.assertEqual(self.dish.average_rating, 4.2)
        self.assertEqual(self.dish.bookmark_count, 10)

    def test_dish_relationship_with_restaurant(self):
        """Test the relationship between Dish and Restaurant."""
        self.assertEqual(self.dish.restaurant.name, "Sample Restaurant")
