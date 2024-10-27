from django.db import models
from django.contrib.auth.models import User
from landing.models import Category, Restaurant, Suggestion
from search.models import Dish
from prodetail.models import Review, ReviewVote
from last_activities.models import Bookmark
from user_profile.models import History

"""
1. Salim => Review , dan ReviewVote
2. Figo => Bookmark
3. Alex => History
4. Rafie => Dish
5. Zillan => Category, Restaurant, 

- Category
- Restaurant     landing
- Dish           search
- Review 
- Review Vote    prodetail
- Bookmark       last_activites
- History        user_profile
"""