from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from main.models import Category, Restaurant, Dish
import json

# Harus di set ulang usernya karena tiap fungsi terisolasi
class SearchTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create categories
        cls.category_italian = Category.objects.create(name="Italian")
        cls.category_japanese = Category.objects.create(name="Japanese")

        # Create restaurants
        cls.restaurant1 = Restaurant.objects.create(
            name="Italiano",
            address="123 Italian St",
            phone="1234567890",
            description="Italian cuisine",
            average_rating=4.5,
            opening_hours="9 AM - 9 PM",
            image="http://example.com/image1.jpg",
            price_range="$$"
        )

        cls.restaurant2 = Restaurant.objects.create(
            name="Sushi Place",
            address="456 Sushi St",
            phone="0987654321",
            description="Japanese cuisine",
            average_rating=4.2,
            opening_hours="10 AM - 10 PM",
            image="http://example.com/image2.jpg",
            price_range="$$$"
        )

        # Create dishes
        Dish.objects.create(
            restaurant=cls.restaurant1,
            category=cls.category_italian,
            name="Pizza",
            description="Classic Italian Pizza",
            average_rating=4.8,
            price=12.99,
            image="http://example.com/pizza.jpg",
            bookmark_count=15
        )

        Dish.objects.create(
            restaurant=cls.restaurant2,
            category=cls.category_japanese,
            name="Sushi Roll",
            description="Fresh Sushi Roll",
            average_rating=4.7,
            price=9.99,
            image="http://example.com/sushi.jpg",
            bookmark_count=20
        )
    
    def test_show_search_page(self):
        # Coba masuk sebelum login
        response = self.client.get(reverse('search'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('search')}")
        
        # Gagal, maka register & login dlu
        User.objects.create_user(username='testuser', password='password123')
        self.client.login(username='testuser', password='password123')
        
        # Coba masuk setelah login
        response = self.client.get(reverse('search'))
        
        # Cek apakah beneran masuk apa nga (di generate templatenya)
        self.assertTemplateUsed(response, 'search_page.html')

    def test_get_dishes_with_post_request(self):
        # Buat Bodynya untuk filtering
        data = {
            'name': 'Sushi Roll',
            'category': self.category_japanese.id,  # Harus id yang dipass
            'price_min': 5,
            'price_max': 15,
            'sort_by': 'cheapest',
            'page': 1
        }
        # Fetch 
        response = self.client.post(
            reverse('get_dishes'),
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Cek apakah sushi roll yang diambil
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['dishes']), 1)
        self.assertEqual(data['dishes'][0]['name'], 'Sushi Roll')
    
    def test_get_dishes_with_get_request(self):
        # Buat URL Search Param nya / Query lalu fetch
        response = self.client.get(reverse('get_dishes'), {
            'name': 'Pizza',
            'category': self.category_italian.id,
            'price_min': 10,
            'price_max': 15,
            'sort_by': 'cheapest',
            'page': 1
        })
        
        # Cek apakah pizaa yang diambil
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['dishes']), 1)
        self.assertEqual(data['dishes'][0]['name'], 'Pizza')
        self.assertEqual(data['dishes'][0]['price'], '12.99')

        # Cek apakah semua komponent pagination 1, karena cuman ada 2 item
        self.assertEqual(int(data['current_page']), 1)
        self.assertEqual(data['min_page'], 1)
        self.assertEqual(data['max_page'], 1)

