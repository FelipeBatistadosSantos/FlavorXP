from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser, CompleteCadastro




class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class CustomUserLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']

class CompleteCadastroForm(forms.ModelForm):
    class Meta:
        model = CompleteCadastro
        fields = ['nascimento','sobre','profissao','hobbie','idioma','comidaf','bebida','restricao', 'cpf','cep','cidade','estado','telefone']