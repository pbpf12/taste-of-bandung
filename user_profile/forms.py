from django.forms import ModelForm
from main.models import User
from django import forms
from django.utils.html import strip_tags

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        }
    
    def clean_name(self):
        username = self.cleaned_data['username']
        return strip_tags(username)
    
    def clean_email(self):
        email = self.cleaned_data['email']
        return strip_tags(email)
    
    def clean_password(self):
        password = self.cleaned_data['password']
        return strip_tags(password)