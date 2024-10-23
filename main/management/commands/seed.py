from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from main.models import Restaurant, Dish, Category, Review, Bookmark, History
from main.management.seeds.users import users_data
from main.management.seeds.contoh import restaurants_contoh, dishes_contoh, reviews_contoh, bookmarks_contoh, history_contoh
from main.management.seeds.rafie import restaurants_rafie, dishes_rafie, reviews_rafie, bookmarks_rafie, history_rafie
from main.management.seeds.figo import *
from main.management.seeds.rahardi import *
from main.management.seeds.alex import *
from main.management.seeds.zillan import *

class Command(BaseCommand):
    help = 'Seed the database with example data for restaurants, dishes, reviews, bookmarks, and history.'

    def handle(self, *args, **kwargs):
        # Seed users
        self.stdout.write(self.style.NOTICE('Seeding Users...'))
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults={'email': user_data['email'], 'password': user_data['password']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created user: {user.username}"))

        # Seed data from contoh and rafie
        self.seed_restaurants_and_dishes(restaurants_contoh, dishes_contoh)
        self.seed_restaurants_and_dishes(restaurants1_figo, dishes1_figo)
        self.seed_restaurants_and_dishes(restaurants2_figo, dishes2_figo)
        self.seed_restaurants_and_dishes(restaurants_rahardi, dishes_rahardi)
        self.seed_restaurants_and_dishes(restaurants_alex, dishes_alex)
        self.seed_restaurants_and_dishes(restaurants_zillan, dishes_zillan)
        self.seed_restaurants_and_dishes(restaurants_rafie,dishes_rafie)

        # Seed reviews from both sources
        self.seed_reviews(reviews_contoh)
        self.seed_reviews(reviews_figo)
        self.seed_reviews(reviews_rahardi)
        self.seed_reviews(reviews_alex)
        self.seed_reviews(reviews_zillan)
        self.seed_reviews(reviews_rafie)

        # Seed bookmarks from both sources
        self.seed_bookmarks(bookmarks_contoh)
        self.seed_bookmarks(bookmarks_figo)
        self.seed_bookmarks(bookmarks_rahardi)
        self.seed_bookmarks(bookmarks_alex)
        self.seed_bookmarks(bookmarks_zillan)
        self.seed_bookmarks(bookmarks_rafie)

        # Seed History
        self.seed_history(history_contoh)
        self.seed_history(history_figo)
        self.seed_history(history_rahardi)
        self.seed_history(history_alex)
        self.seed_history(history_zillan)
        self.seed_history(history_rafie)

        self.stdout.write(self.style.SUCCESS('Seeding completed successfully!'))

    def seed_restaurants_and_dishes(self, restaurant_data_list, dish_data_list):
        self.stdout.write(self.style.NOTICE('Seeding Restaurants and Dishes...'))
        for restaurant_data in restaurant_data_list:
            restaurant, created = Restaurant.objects.get_or_create(
                name=restaurant_data['name'],
                defaults={
                    'address': restaurant_data['address'],
                    'phone': restaurant_data['phone'],
                    'description': restaurant_data['description'],
                    'opening_hours': restaurant_data['opening_hours'],
                    'image': restaurant_data['image'],
                    'price_range': ''  # Price range will be calculated later
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created restaurant: {restaurant.name}"))

        for dish_data in dish_data_list:
            restaurant = Restaurant.objects.get(name=dish_data['restaurant'])
            category, _ = Category.objects.get_or_create(name=dish_data['category'])
            dish, created = Dish.objects.get_or_create(
                restaurant=restaurant,
                category=category,
                name=dish_data['name'],
                defaults={
                    'description': dish_data['description'],
                    'price': dish_data['price'],
                    'image': dish_data['image']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created dish: {dish.name} for restaurant: {restaurant.name}"))

            # Update the restaurant's price range
            self.update_restaurant_price_range(restaurant)

    def seed_reviews(self, review_data_list):
        self.stdout.write(self.style.NOTICE('Seeding Reviews...'))
        for review_data in review_data_list:
            user = User.objects.get(username=review_data['user'])
            restaurant = Restaurant.objects.get(name=review_data['restaurant'])
            dish = Dish.objects.get(name=review_data['dish'])
            review, created = Review.objects.get_or_create(
                user=user,
                restaurant=restaurant,
                dish=dish,
                defaults={
                    'rating': review_data['rating'],
                    'comment': review_data['comment'],
                    'upvotes': review_data.get('upvotes', 0),
                    'downvotes': review_data.get('downvotes', 0)
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created review for dish: {dish.name} by {user.username}"))

            # Update the average rating of the dish and the restaurant
            self.update_dish_average_rating(dish)
            self.update_restaurant_average_rating(restaurant)

    def seed_bookmarks(self, bookmark_data_list):
        self.stdout.write(self.style.NOTICE('Seeding Bookmarks...'))
        for bookmark_data in bookmark_data_list:
            user = User.objects.get(username=bookmark_data['user'])
            restaurant = Restaurant.objects.get(name=bookmark_data['restaurant']) if bookmark_data['restaurant'] else None
            dish = Dish.objects.get(name=bookmark_data['dish'])
            bookmark, created = Bookmark.objects.get_or_create(
                user=user,
                restaurant=restaurant,
                dish=dish
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created bookmark for {dish.name} by {user.username}"))

            # Update the bookmark count for the dish
            dish.bookmark_count = Bookmark.objects.filter(dish=dish).count()
            dish.save()

    def update_restaurant_price_range(self, restaurant):
        # Calculate price range (min - max price) for the restaurant
        prices = restaurant.dish_set.values_list('price', flat=True)
        if prices:
            min_price, max_price = min(prices), max(prices)
            price_range = f"Rp{min_price} - Rp{max_price}"
            restaurant.price_range = price_range
            restaurant.save()
            self.stdout.write(self.style.SUCCESS(f"Updated price range for restaurant: {restaurant.name}"))

    def update_dish_average_rating(self, dish):
        # Calculate and update average rating for the dish
        ratings = dish.review_set.values_list('rating', flat=True)
        if ratings:
            average_rating = sum(ratings) / len(ratings)
            dish.average_rating = round(average_rating, 2)
            dish.save()
            self.stdout.write(self.style.SUCCESS(f"Updated average rating for dish: {dish.name}"))

    def update_restaurant_average_rating(self, restaurant):
        # Calculate and update average rating for the restaurant
        ratings = restaurant.review_set.values_list('rating', flat=True)
        if ratings:
            average_rating = sum(ratings) / len(ratings)
            restaurant.average_rating = round(average_rating, 2)
            restaurant.save()
            self.stdout.write(self.style.SUCCESS(f"Updated average rating for restaurant: {restaurant.name}"))

    def seed_history(self, history_data):
        self.stdout.write(self.style.NOTICE('Seeding History...'))
        for history_item in history_data:
            try:
                user = User.objects.get(username=history_item['user'])
                dish = Dish.objects.get(name=history_item['dish']) if history_item['dish'] else None
            except (User.DoesNotExist, Dish.DoesNotExist) as e:
                self.stdout.write(self.style.ERROR(f"Error finding data for history: {e}. History skipped."))
                continue

            History.objects.get_or_create(
                user=user,
                dish=dish
            )
            self.stdout.write(self.style.SUCCESS(f"Created history for dish: {dish.name if dish else 'None'} by {user.username}"))
