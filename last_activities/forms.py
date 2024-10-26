from django import forms

class ActivityFilterForm(forms.Form):
    ACTIVITY_CHOICES = [
        ('bookmark', 'Bookmarks'),
    ]
    activity_type = forms.ChoiceField(choices=ACTIVITY_CHOICES, required=False, label='Activity Type')
