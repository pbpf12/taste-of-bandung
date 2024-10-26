from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.http import JsonResponse
import json
from main.models import History, Dish, Restaurant, Category
from user_profile.views import show_json, show_profile, delete_user, edit_profile, show_history_as_json, clear_history

class UnitTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(
            username='testuser',
            first_name='Test',
            last_name='User',
            email='testuser@example.com',
            password='password123'
        )
        # Set up the request factory
        self.factory = RequestFactory()
        
        # Create a category for dishes
        self.category = Category.objects.create(name="Test Category")

    def setup_request(self, request):
        """Adds session and message middleware to request"""
        middleware = SessionMiddleware(lambda x: None)
        middleware.process_request(request)
        request.session.save()
        
        # Add messages middleware
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)

    def test_show_json_view(self):
        request = self.factory.get('/show_json/')
        request.user = self.user
        self.setup_request(request)

        response = show_json(request)
        
        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 200)
        
        response_data = json.loads(response.content)
        self.assertEqual(response_data['username'], 'testuser')
        self.assertEqual(response_data['first_name'], 'Test')
        self.assertEqual(response_data['last_name'], 'User')
        self.assertEqual(response_data['email'], 'testuser@example.com')

    def test_show_profile_view_with_incomplete_profile(self):
        self.user.first_name = ''
        self.user.save()

        request = self.factory.get(reverse('profile'))
        request.user = self.user
        self.setup_request(request)

        response = show_profile(request)

        self.assertEqual(response.status_code, 200)
        messages = list(get_messages(request))
        self.assertTrue(any("Your profile is incomplete" in str(message) for message in messages))

    def test_delete_user_view(self):
        request = self.factory.post(reverse('delete_user'))
        request.user = self.user
        self.setup_request(request)

        response = delete_user(request)

        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username='testuser')

        messages = list(get_messages(request))
        self.assertTrue(any("Your account has been deleted." in str(message) for message in messages))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('login'))

    def test_edit_profile_view_success(self):
        request = self.factory.post(reverse('edit_profile'), {
            'first_name': 'Updated',
            'last_name': 'User',
            'email': 'updated@example.com'
        })
        request.user = self.user
        self.setup_request(request)

        response = edit_profile(request)

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 200)

        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.email, 'updated@example.com')

        response_data = json.loads(response.content)
        self.assertEqual(response_data['status'], 'success')
        self.assertEqual(response_data['user']['first_name'], 'Updated')

    def test_show_history_as_json_view(self):
        # Create test data
        restaurant = Restaurant.objects.create(name="Testaurant")
        dish = Dish.objects.create(
            name="Test Dish", 
            restaurant=restaurant, 
            price=10.99,
            category=self.category  # Add the required category
        )
        history_record = History.objects.create(user=self.user, dish=dish)

        request = self.factory.get(reverse('show_history'))
        request.user = self.user
        self.setup_request(request)

        response = show_history_as_json(request)

        self.assertIsInstance(response, JsonResponse)
        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.content)
        self.assertEqual(len(response_data['history']), 1)
        self.assertEqual(response_data['history'][0]['dish']['name'], "Test Dish")

    def test_clear_history_view(self):
        # Create test data
        restaurant = Restaurant.objects.create(name="Testaurant")
        dish = Dish.objects.create(
            name="Test Dish", 
            restaurant=restaurant, 
            price=10.99,
            category=self.category  # Add the required category
        )
        History.objects.create(user=self.user, dish=dish)

        request = self.factory.post(reverse('clear_history'))
        request.user = self.user
        self.setup_request(request)

        response = clear_history(request)

        self.assertEqual(History.objects.filter(user=self.user).count(), 0)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('show_history'))