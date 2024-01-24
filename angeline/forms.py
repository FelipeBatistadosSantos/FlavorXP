from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser




class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class CustomUserLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']