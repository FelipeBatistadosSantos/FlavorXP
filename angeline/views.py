from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import logout, authenticate, login as auth_login
from django.contrib import messages
from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserLoginForm
from django.contrib.auth.views import LoginView



def cadastro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Cadastro realizado com sucesso. Faça o login.')
            return redirect('angeline:login')
        else:
            messages.error(request, 'Erro no cadastro. Por favor, corrija os erros abaixo.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register/cadastro.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'register/login.html'
    authentication_form = CustomUserLoginForm



def home(request):
    return render(request, 'angeline/home.html')


def host(request):
    return render(request, 'angeline/host.html')

def sair(request):
    logout(request)
    return redirect('main:base')


def perfil(request):
    return render(request, )





def testeFeed(request):
    lista = {'nome':'Jardinagem', }

    return render(request, 'angeline/home.html')