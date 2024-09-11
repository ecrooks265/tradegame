from django import forms
from django.contrib.auth.models import User
from tradeapp.models import *

class UserSignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class GameCreationForm(forms.ModelForm):
    DURATION_CHOICES = [
        (3, '3 Minutes'),
        (5, '5 Minutes'),
        (10, '10 Minutes'),
    ]

    duration = forms.ChoiceField(
        choices=DURATION_CHOICES, 
        widget=forms.RadioSelect,  # radio buttons
        label='Select Game Duration'
    )

    class Meta:
        model = Game
        fields = ['name', 'duration']
