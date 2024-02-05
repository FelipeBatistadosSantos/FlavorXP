from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomUser, CompleteCadastro, Host, Evento
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from localflavor.br.forms import BRZipCodeField, BRCPFField
from phonenumber_field.modelfields import PhoneNumberField
import json


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


class DateInput(forms.DateInput):
    input_type = 'text'
    format = '%d/%m/%Y'
    attrs = {'placeholder': '__/__/____'}

class CompleteCadastroForm(forms.ModelForm):
    
    nascimento = forms.DateField(label=_('Data de Nascimento:'), input_formats=["%d/%m/%Y",], widget=DateInput())
    sobre = forms.CharField(label='Fale um pouco sobre você: ', widget=forms.Textarea)
    idioma = forms.ChoiceField(label='Você conhece outro idioma? ', choices=CompleteCadastro.IDIOMA_CHOICES)
    comidaf = forms.CharField(label='Comida favorita: ')
    bebida = forms.CharField(label='Bebida favorita')
    restricao = forms.ChoiceField(label='Você possui alguma restrição? ', choices=CompleteCadastro.RESTRICAO_CHOICES)
    cpf = BRCPFField()
    cep = BRZipCodeField()
    telefone = PhoneNumberField()
    outra_restricao = forms.CharField(label='Informe ')

        
    class Meta:
        model = CompleteCadastro
        fields = ['nascimento', 'sobre', 'profissao', 'hobbie', 'idioma', 'comidaf', 'bebida', 'restricao', 'outra_restricao', 'cpf', 'cep', 'cidade', 'estado', 'telefone']

        
   
        
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

    class Meta:
        model = Evento
        fields = ['estilo','tema','fotos','host','descricao','cardapio','inclui_bebidas','bebidas_oferecidas','convidado_pode_trazer',
                  'max_convidados','local','data','horario','valor_host',]
        
        widgets = {
            'horario': forms.TimeInput(format='%H:%M', attrs={'type': 'time'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(EventoForm, self).__init__(*args, **kwargs)
