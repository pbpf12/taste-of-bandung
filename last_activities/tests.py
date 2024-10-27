from django.test import TestCase
from django.urls import reverse
from main.models import User, Restaurant, Dish, Bookmark

class LastActivitiesPageTest(TestCase):
    def test_last_activities_page_renders_correct_template(self):
        response = self.client.get(reverse('last_activities_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'last_activities_page.html')

    def test_delete_bookmark_successful(self):
        # Create a user and bookmark
        user = User.objects.create_user(username='testuser', password='testpass')
        bookmark = Bookmark.objects.create(user=user)

        # Log in the user
        self.client.login(username='testuser', password='testpass')

        # Send POST request to delete the bookmark
        response = self.client.post(reverse('delete_bookmark'), {'id': bookmark.id})
        
        # Assert response and deletion
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'Bookmark deleted successfully')
    
    def test_last_activities_view(self):
        # Create a user and log them in
        user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        # Create a bookmark
        Bookmark.objects.create(user=user)

        # Make GET request to the view
        response = self.client.get(reverse('last_activities'))
        
        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertIn('bookmarks', response.json())
    


