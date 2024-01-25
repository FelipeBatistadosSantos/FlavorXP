from django import forms
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    senha = forms.CharField(label='Senha', widget=forms.PasswordInput)
    

class CadastroForm(forms.Form):
    nome = forms.CharField(label='Nome', max_length=100, required=True)
    email = forms.EmailField(label='Email', max_length=100, required=True)
    cpf = forms.CharField(label='Cpf', max_length=11, required=True)
    telefone = forms.CharField(label='Telefone', max_length=15, required=True)
    cidade = forms.CharField(label='Cidade', max_length=30, required=True)
    estado = forms.CharField(label='Estado', max_length=30, required=True)
    senha = forms.CharField(label='Senha', widget=forms.PasswordInput, required=True)
    confirmar_senha = forms.CharField(label='Confirmar Senha', widget=forms.PasswordInput, required=True)

    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        if nome and len(nome) < 3:
            raise forms.ValidationError('Nome inválido')
        return nome

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if cpf and len(cpf) < 11:
            raise forms.ValidationError('Cpf inválido')
        return cpf

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if telefone and len(telefone) < 11:
            raise ValidationError('Telefone inválido')
        return telefone

    def clean_senha(self):
        senha = self.cleaned_data.get('senha')
        if senha and len(senha) < 8:
            raise forms.ValidationError('A senha deve ter pelo menos 8 caracteres.')
        return senha

    def clean_confirmar_senha(self):
        senha = self.cleaned_data.get('senha')
        confirmar_senha = self.cleaned_data.get('confirmar_senha')

        if senha and confirmar_senha and senha != confirmar_senha:
            raise forms.ValidationError('As senhas não coincidem.')

        return confirmar_senha
