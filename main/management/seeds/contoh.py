# restaurant_{nama}
restaurants_contoh = [
    {
        "name": "Rumah Makan Padang Malah Dicubo",
        "address": "Jl. Padang Indah No.123",
        "phone": "081234567890",
        "description": "Restoran Padang terkenal di kota ini.",
        "opening_hours": "08:00 - 20:00",
        "image": "https://example.com/restaurant-image.jpg",
        "price_range": ""
    },
    {
        "name": "Warung Makan Sederhana",
        "address": "Jl. Jendral Sudirman No.456",
        "phone": "081987654321",
        "description": "Makanan sederhana dengan harga terjangkau.",
        "opening_hours": "10:00 - 22:00",
        "image": "https://example.com/restaurant-image-2.jpg",
        "price_range": ""
    }
]

# dishes_{nama}
dishes_contoh = [
    {
        "name": "Nasi Gulai Babat",
        "description": "Nasi Campur Sayur Dan Sambel + gulai babat",
        "price": 35000,
        "image": "https://example.com/nasi-gulai-babat.jpg",
        "category": "Food",  # Reference by name
        "restaurant": "Rumah Makan Padang Malah Dicubo"  # Reference by name
    },
    {
        "name": "Es Teh Manis",
        "description": "Teh manis dingin yang menyegarkan.",
        "price": 5000,
        "image": "https://example.com/es-teh-manis.jpg",
        "category": "Drink",  # Reference by name
        "restaurant": "Rumah Makan Padang Malah Dicubo"  # Reference by name
    }
]

# reviews_{nama}
reviews_contoh = [
    {
        'user': 'user1',
        'restaurant': 'Rumah Makan Padang Malah Dicubo',
        'dish': 'Es Teh Manis',
        'rating': 5,
        'comment': 'Luar biasa! Es Teh Mansi seger menyegarkan.',
        'upvotes': 20,
        'downvotes': 1
    },
    {
        'user': 'user2',
        'restaurant': 'Rumah Makan Padang Malah Dicubo',
        'dish': 'Nasi Gulai Babat',
        'rating': 4,
        'comment': 'Babatnya lembut, rasanya enak, tapi kurang pedas.',
        'upvotes': 15,
        'downvotes': 2
    }
]

# history_{nama}
history_contoh = [
    {
        'user': 'user1',
        'dish': 'Es Teh Manis'
    },
    {
        'user': 'user2',
        'dish': 'Nasi Gulai Babat'
    },
        {
        'user': 'user1',
        'dish': 'Es Teh Manis'
    },
    {
        'user': 'user2',
        'dish': 'Nasi Gulai Babat'
    },    {
        'user': 'user1',
        'dish': 'Es Teh Manis'
    },
    {
        'user': 'user2',
        'dish': 'Nasi Gulai Babat'
    },
]

# bookmarks_{nama}
bookmarks_contoh = [
    {
        'user': 'user1',
        'restaurant': "Rumah Makan Padang Malah Dicubo",
        'dish': 'Es Teh Manis'
    },
    {
        'user': 'user2',
        'restaurant': "Rumah Makan Padang Malah Dicubo",
        'dish': 'Nasi Gulai Babat'
    },
    {
        'user': 'user2',
        'restaurant': "Rumah Makan Padang Malah Dicubo",
        'dish': 'Nasi Gulai Babat'
    },
]

