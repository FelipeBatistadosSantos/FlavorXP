from django.shortcuts import render, HttpResponse, redirect
from .models import CustomUser
from .forms import CadastroForm, LoginForm

def cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        email = request.POST['email']
        nome = request.POST['nome']
        senha = request.POST['senha']
        telefone = request.POST['telefone']

        usuario = CustomUser.objects.create_user(email=email, password=senha, nome=nome, telefone=telefone)
        usuario.save()
        return redirect('angeline:login')  # Redireciona para a página de login após o cadastro
    else:
        form = CadastroForm()
    
    return render(request, 'angeline/cadastro.html', {'form': form})  # Renderiza o formulário de cadastro


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        email = request.POST['email']
        senha = request.POST['senha']
        try:
            usuario = CustomUser.objects.get(email=email)
            if usuario.check_password(senha):
               
                return HttpResponse('Entrou')  # Redireciona para a página inicial após o login bem-sucedido
            else:
               
                return render(request, 'angeline/login.html', {'form': form,})
            
        except CustomUser.DoesNotExist:
            
            return render(request, 'angeline/login.html', {'form': form})
    else:
        form = LoginForm()
    
    return render(request, 'angeline/login.html', {'form':form})

