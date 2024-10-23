from django import forms

class ActivityFilterForm(forms.Form):
    ACTIVITY_CHOICES = [
        ('all', 'All Activities'),
        ('review', 'Reviews'),
        ('bookmark', 'Bookmarks'),
        ('history', 'History'),
    ]
    activity_type = forms.ChoiceField(choices=ACTIVITY_CHOICES, required=False, label='Activity Type')