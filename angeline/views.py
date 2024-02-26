from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth import logout, authenticate, login as auth_login
from django.contrib import messages
from .models import CompleteCadastro,Host, Evento, Reserva
from .forms import CustomUserCreationForm, CustomUserLoginForm, CompleteCadastroForm, HostForm, EventoForm, AgendamentoForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.views import View


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


@login_required
def home(request):
    perfil_usuario = CompleteCadastro.objects.filter(usuario=request.user).first()
    eventos = Evento.objects.all()

    if perfil_usuario: 
        if perfil_usuario.is_complete():  
            return render(request, 'angeline/home.html', {'eventos': eventos,'perfil_usuario': perfil_usuario, 'form_preenchido': True})
        else:
            return render(request, 'angeline/home.html', {'eventos': eventos,'form_preenchido': False})
    else:
        return render(request, 'angeline/home.html', {'eventos': eventos,'form_preenchido': False})


    


@login_required
def host(request):
    user = request.user

    if Host.objects.filter(usuario=user).exists():
        return redirect('angeline:perfil_host')
    else:
        return redirect('angeline:editar_host')
    
    
@login_required
def perfil(request):
    perfil_usuario = CompleteCadastro.objects.filter(usuario=request.user).first()

    try:
        host = request.user.host
    except Host.DoesNotExist:
        host = None

    created = False

    if 'edit' in request.GET:
        return redirect('angeline:editar_perfil')

    if request.method == 'POST':
        form = CompleteCadastroForm(request.POST, request.FILES, instance=perfil_usuario)
        if form.is_valid():
            if not perfil_usuario:
                perfil_usuario = form.save(commit=False)
                perfil_usuario.usuario = request.user
                perfil_usuario.save()
                created = True
            else:
                form.save()

            return redirect('angeline:perfil')
    else:
        form = CompleteCadastroForm(instance=perfil_usuario)

    user_email = request.user.email if request.user else None

    return render(request, 'angeline/perfil.html', {'form': form, 'perfil_usuario': perfil_usuario, 'host': host, 'form_preenchido': not created, 'user_email': user_email})



def completar_perfil(request):
    if request.method == 'POST':
        form = CompleteCadastroForm(request.POST, request.FILES)
        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.usuario = request.user  
            perfil.save()
            return redirect('angeline:perfil')
    else:
        form = CompleteCadastroForm()
    
    return render(request, 'angeline/completar_perfil.html', {'form': form})




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


@login_required
def evento(request):
    perfil_usuario, created = CompleteCadastro.objects.get_or_create(usuario=request.user)

    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES) 
        if form.is_valid():
            evento = form.save(commit=False)
            evento.host, created = Host.objects.get_or_create(usuario=request.user, defaults={'nome_empresa': 'Nome da Empresa Padrão'})
            evento.save()  
            form.save_m2m()  
            messages.success(request, 'Evento criado com sucesso!')
            return redirect('angeline:home') 
    else:
        form = EventoForm()

    eventos = Evento.objects.all()

    return render(request, 'angeline/evento.html', {'form': form, 'perfil_usuario': perfil_usuario, 'eventos': eventos})




def specific_page(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)

    context = {
        'evento': evento,
    }

    return render(request, 'angeline/specific_page.html', context)


def criar_host(request):
    if request.method == 'POST':
        form = HostForm(request.POST)
        if form.is_valid():
            host = form.save(commit=False)
            host.usuario = request.user
            host.save()
            return redirect('angeline:perfil')
    else:
        form = HostForm()
    return render(request, 'angeline/criar_host.html', {'form': form})


@login_required
def editar_host(request):
    host, created = Host.objects.get_or_create(usuario=request.user)
    if request.method == 'POST':
        form = HostForm(request.POST, request.FILES, instance=host)
        if form.is_valid():
            form.save()
            messages.success(request, 'Informações do host atualizadas com sucesso!')
            return redirect('angeline:host')  
    else:
        form = HostForm(instance=host)
    return render(request, 'angeline/editar_host.html', {'form': form, 'host': host, 'form_preenchido': not created})


@login_required
def perfil_host(request):
    host, created = Host.objects.get_or_create(usuario=request.user)

    if 'edit' in request.GET:
        return redirect('angeline:editar_host')

    if request.method == 'POST':
        form = HostForm(request.POST, request.FILES, instance=host)
        if form.is_valid():
            form.save()

            if created:
                return redirect('angeline:perfil_host')
    else:
        form = HostForm(instance=host)

    return render(request, 'angeline/host.html', {'form': form, 'host': host, 'form_preenchido': not created})


def host_servico(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)
    
    context = {
        'evento': evento,
    }
    
    return render(request, 'angeline/host_servico.html', context)
    

@login_required
def editar_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id)

    if request.user != evento.host.usuario:
        return redirect('angeline:home')

    if request.method == 'POST':
        form = EventoForm(request.POST, request.FILES, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('angeline:specific_page', evento_id=evento.id)
    else:
        form = EventoForm(instance=evento)

    return render(request, 'angeline/editar_evento.html', {'form': form, 'evento': evento})



@login_required
def agendar_evento(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.usuario = request.user
            reserva.evento = evento
            reserva.save()
            
            return redirect('angeline:lista_reservas')
    else:
        form = AgendamentoForm()
    
    return render(request, 'angeline/agendar_evento.html', {'form': form, 'evento': evento})

@login_required
def lista_reservas(request):
    reservas = Reserva.objects.filter(usuario=request.user)
    return render(request, 'angeline/lista_reservas.html', {'reservas': reservas})


@login_required
def cancelar(request, agendamento_id):
    reserva = get_object_or_404(Reserva, id=agendamento_id, usuario=request.user)
    evento = reserva.evento
    reserva.delete()
    
    return redirect('angeline:lista_reservas')


@login_required
def excluir_evento(request, evento_id):
    evento = get_object_or_404(Evento, id=evento_id, host__usuario=request.user)
    evento.delete() 
<<<<<<< HEAD
    return redirect('angeline:home')



def cardapio(request):
    return render(request, 'angeline/cardapio.html')
=======
    return redirect('angeline:gerenciamento')


@login_required
def gerenciamento(request):
    eventos = Evento.objects.filter(host=request.user.host)
    return render(request, 'angeline/gerenciamento.html', {'eventos': eventos})
>>>>>>> dev-luana
