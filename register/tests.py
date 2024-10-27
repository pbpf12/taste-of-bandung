from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from main.models import Category, Restaurant, Dish
import json

# Create your tests here.
class RegisterTest(TestCase):
    def test_register_user(self):
        # Register user
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
        })
        
        # Cek apakah user berhasil dibuat
        user_exists = User.objects.filter(username='newuser').exists()
        self.assertTrue(user_exists)
