from django import forms
from django.contrib.auth.models import User
from tradeapp.models import *

class UserSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class GameCreationForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'duration']  # Adjust fields as needed