from django import forms

class SearchForm(forms.Form):
    name = forms.CharField(required=False)
    type = forms.CharField(required=False)
    price_min = forms.IntegerField(required=False)
    price_max = forms.IntegerField(required=False)
    category = forms.CharField(required=False)
    sort_by = forms.CharField(required=False)
