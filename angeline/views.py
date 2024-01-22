from django.shortcuts import render, HttpResponse, redirect
from .models import CustomUser
from .forms import CadastroForm, LoginForm

def cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            nome = request.POST['nome']
            cpf = request.POST['cpf']
            senha = request.POST['senha']
            telefone = request.POST['telefone']
            cidade = request.POST['cidade']
            estado = request.POST['estado']

            usuario = CustomUser.objects.create_user(email=email, password=senha, nome=nome, telefone=telefone, cidade=cidade, cpf=cpf, estado=estado)
            usuario.save()
            return redirect('angeline:login')
        else:
            erros = form.errors
            return render(request, 'angeline/cadastro.html', {'form': form, 'erros': erros})  
    else:
        form = CadastroForm()
    
    return render(request, 'angeline/cadastro.html', {'form': form})  


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        email = request.POST['email']
        senha = request.POST['senha']
        try:
            usuario = CustomUser.objects.get(email=email)
            if usuario.check_password(senha):
               
                return redirect('angeline:home')  # Redireciona para a página inicial após o login bem-sucedido
            else:
               
                return render(request, 'angeline/login.html', {'form': form,})
            
        except CustomUser.DoesNotExist:
            
            return render(request, 'angeline/login.html', {'form': form})
    else:
        form = LoginForm()
    
    return render(request, 'angeline/login.html', {'form':form})

def home(request):
    return render(request, 'angeline/home.html')