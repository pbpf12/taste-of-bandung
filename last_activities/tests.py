# from django.test import TestCase
# from django.urls import reverse

# class LastActivitiesTests(TestCase):

#     def test_last_activities_view(self):
#         # Call the view using the URL name
#         response = self.client.get(reverse('last_activities'))
        
#         # Check that the response is 200 OK
#         self.assertEqual(response.status_code, 200)

#         # Check that the returned data is a JSON format and has expected keys
#         json_data = response.json()
#         self.assertIn('bookmarks', json_data)
#         self.assertEqual(len(json_data['bookmarks']), 2)  # Since we mocked 2 bookmarks

#     def test_last_activities_page(self):
#         # Call the page view
#         response = self.client.get(reverse('last_activities_page'))

#         # Check that the response is 200 OK
#         self.assertEqual(response.status_code, 200)

#         # Check if the header is present in the rendered content
#         self.assertContains(response, "Last Bookmarked Dishes")
