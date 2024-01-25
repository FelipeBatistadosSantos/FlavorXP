from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser




class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        # Remover mensagens de validação padrão
        for field in self.fields.values():
            field.widget.attrs.pop("title", None)
            field.help_text = None

        # Adicionar placeholders se desejar
        self.fields['username'].widget.attrs['placeholder'] = 'Usuário'
        self.fields['email'].widget.attrs['placeholder'] = 'Endereço de email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Senha'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirmação de senha'
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class CustomUserLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'password']