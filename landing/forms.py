from django.forms import ModelForm
from landing.models import Suggestion
from django import forms
from django.utils.html import strip_tags

class SuggestionForm(ModelForm):
    class Meta:
        model = Suggestion
        fields = ["suggestionMessage"]

    def clean_suggestion(self):
        suggestionMessage = self.cleaned_data["suggestionMessage"]
        return strip_tags(suggestionMessage)