from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import logout, authenticate, login as auth_login
from django.contrib import messages
from .models import CustomUser, CompleteCadastro
from .forms import CustomUserCreationForm, CustomUserLoginForm, CompleteCadastroForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from .models import Produto
from .forms import ProdutoFilterForm



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


class CustomLogoutView(LogoutView):
    next_page = 'main:base'



def home(request):
    return render(request, 'angeline/home.html')


def host(request):
    return render(request, 'angeline/host.html')





@login_required
def perfil(request):
    perfil_usuario, created = CompleteCadastro.objects.get_or_create(usuario=request.user)

    if 'edit' in request.GET:
        return redirect('angeline:editar_perfil')

    if request.method == 'POST':
        form = CompleteCadastroForm(request.POST, request.FILES, instance=perfil_usuario)
        if form.is_valid():
            form.save()
            
            if created:
                return redirect('angeline:perfil')
    else:
        form = CompleteCadastroForm(instance=perfil_usuario)

    return render(request, 'angeline/perfil.html', {'form': form, 'perfil_usuario': perfil_usuario, 'form_preenchido': not created})


@login_required
def editar_perfil(request):
    perfil_usuario, created = CompleteCadastro.objects.get_or_create(usuario=request.user)

    if request.method == 'POST':
        form = CompleteCadastroForm(request.POST, request.FILES, instance=perfil_usuario)
        if form.is_valid():
            form.save()
            return redirect('angeline:perfil')  
    else:
        form = CompleteCadastroForm(instance=perfil_usuario)

    return render(request, 'angeline/editar_perfil.html', {'form': form, 'perfil_usuario': perfil_usuario})



def testeFeed(request):
    lista = {'nome':'Jardinagem', }

    return render(request, 'angeline/home.html')


def listar_produtos(request):
    produtos = Produto.objects.all()
    form = ProdutoFilterForm(request.GET)

    if form.is_valid():
        cidade = form.cleaned_data.get('cidade')

        if cidade:
            produtos = produtos.filter(cidade__icontains=cidade)

    return render(request, 'angeline/filtro.html', {'produtos': produtos, 'form': form})