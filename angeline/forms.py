from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser, CompleteCadastro


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    senha = forms.CharField(label='Senha', widget=forms.PasswordInput)
    

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

        return confirmar_senha

class CompleteCadastroForm(forms.ModelForm):
    class Meta:
        model = CompleteCadastro
        fields = ['nascimento','sobre','profissao','hobbie','idioma','comidaf','bebida','restricao', 'cpf','cep','cidade','estado','telefone']