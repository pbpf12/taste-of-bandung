from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from main.models import Category, Restaurant, Dish
import json

class LoginTest(TestCase):

    def test_login_user(self):
        # Register dengan fungsi sebelumnya
        user = User.objects.create_user(username="newuser", password="newpassword123")

        # Log in user
        response = self.client.post(reverse('login'), {
            'username': 'newuser',
            'password': 'newpassword123',
        })
        
        # Cek apakah cookies sudah di set
        self.assertNotEqual(response.cookies['last_login'].value, '')

    def test_logout_user(self):
        # Register dan Login dengan fungsi sebelumnya
        user = User.objects.create_user(username="newuser", password="newpassword123")
        self.client.login(username='newuser', password='newpassword123')

        # Log out
        response = self.client.get(reverse('logout'))

        # Cek apakah cookies sudah di-delete
        self.assertTrue('last_login' in response.cookies)
        self.assertEqual(response.cookies['last_login'].value, '')