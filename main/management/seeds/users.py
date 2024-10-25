# nga usah diapa-apain
# Data Dummy Users

from django.contrib.auth.hashers import make_password

users_data = [
    {
        'username': 'user1',
        'email': 'user1@example.com',
        'password': make_password('password123')  # password di-hash
    },
    {
        'username': 'user2',
        'email': 'user2@example.com',
        'password': make_password('password123')  # password di-hash
    }
]
