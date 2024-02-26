from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomUser, CompleteCadastro, Host, Evento, Agendamento
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext as __
import datetime
from django.utils import timezone
from localflavor.br.forms import BRZipCodeField, BRCPFField
from phonenumber_field.modelfields import PhoneNumberField
import json
from geopy.geocoders import Nominatim

class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.pop("title", None)
            field.help_text = None

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

    def clean_confirmar_senha(self):
        senha = self.cleaned_data.get('senha')
        confirmar_senha = self.cleaned_data.get('confirmar_senha')

        if senha and confirmar_senha and senha != confirmar_senha:
            raise forms.ValidationError('As senhas não coincidem.')

        return confirmar_senha

    

class DateInput(forms.DateInput):
    input_type = 'text'
    format = '%d/%m/%Y'
    attrs = {'placeholder': '__/__/____'}

class CompleteCadastroForm(forms.ModelForm):
    
    nascimento = forms.DateField(label=_('Data de Nascimento:'), input_formats=["%d/%m/%Y",], widget=DateInput())
    sobre = forms.CharField(label='Fale um pouco sobre você: ', widget=forms.Textarea, max_length=359)
    idioma = forms.ChoiceField(label='Você conhece outro idioma? ', choices=CompleteCadastro.IDIOMA_CHOICES)
    comidaf = forms.CharField(label='Comida favorita: ')
    bebida = forms.CharField(label='Bebida favorita')
    restricao = forms.ChoiceField(label='Você possui alguma restrição? ', choices=CompleteCadastro.RESTRICAO_CHOICES)
    cpf = BRCPFField()
    cep = BRZipCodeField()
    telefone = PhoneNumberField()
    
        
    class Meta:
        model = CompleteCadastro
        fields = ['foto','nascimento', 'sobre', 'profissao', 'hobbie', 'idioma', 'comidaf', 'bebida', 'restricao','cpf', 'cep', 'cidade', 'estado', 'telefone']

        
   
        
    def clean_nascimento(self):
        nascimento = self.cleaned_data.get('nascimento')

        if nascimento and nascimento > timezone.now().date():
            raise ValidationError(_('A data de nascimento não pode ser no futuro.'))

        return nascimento

class HostForm(forms.ModelForm):
    class Meta:
        model = Host
        fields = ['nome_empresa', 'motivo', 'area_gastronomia', 'servicos', 'frequencia_servicos', 'local_servico', 'descricao_local']


class CustomDecimalField(forms.RegexField):
    def __init__(self, **kwargs):
        
        kwargs['regex'] = r'^(\d+(\.\d{1,2})?|\d+,\d{2})?$'

        super().__init__(**kwargs)



class EventoForm(forms.ModelForm):

    valor_host = CustomDecimalField(label='Valor do Host')
    restricao = forms.ChoiceField(label='Alimentos para alguma restrição? ', choices=Evento.RESTRICAO_CHOICES)


    class Meta:
        model = Evento
        fields = ['estilo','tema','fotos','descricao','cardapio','inclui_bebidas','bebidas_oferecidas','convidado_pode_trazer',
                  'max_convidados','local','data','horario','valor_host','restricao']
        

        widgets = {
            'fotos': forms.FileInput(),
            'horario': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(EventoForm, self).__init__(*args, **kwargs)
        
    # importing geopy library and Nominatim class
    

    @staticmethod
    def geo(address):
        loc = Nominatim(user_agent="Geopy Library")
        location = loc.geocode(address)
        if location:
            print(location.address)
            print("Latitude = ", location.latitude)
            print("Longitude = ", location.longitude)
        else:
            print("Endereço não encontrado.")

    def clean(self):
        cleaned_data = super().clean()
        address = cleaned_data.get("local")
        self.geo(address)
        return cleaned_data
    
class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['quantidade_pessoas', 'nomes_convidados']

    def __init__(self, *args, **kwargs):
        self.evento_id = kwargs.pop('evento_id', None)
        super().__init__(*args, **kwargs)
        self.fields['quantidade_pessoas'].widget.attrs['min'] = 1  
        self.fields['quantidade_pessoas'].widget.attrs['max'] = self.get_max_vagas() 
    def get_max_vagas(self):
        if self.evento_id:
            evento = Evento.objects.get(pk=self.evento_id)
            return evento.vagas_disponiveis
        return 0

    def clean_quantidade_pessoas(self):
        quantidade_pessoas = self.cleaned_data['quantidade_pessoas']
        max_vagas = self.get_max_vagas()
        if quantidade_pessoas > max_vagas:
            raise forms.ValidationError(f'Não há vagas suficientes disponíveis. Máximo de {max_vagas} vagas.')
        return quantidade_pessoas
