from django.urls import path
from django.contrib.auth.views import LoginView
from .views import cadastro, CustomLoginView, home, host, perfil

app_name = 'angeline'

urlpatterns = [
    path('cadastro', cadastro, name='cadastro'),
    path('login', CustomLoginView.as_view(), name='login'),
    path('home', home, name='home'),
    path('seja host', host, name='host'),
    path('perfil', perfil, name='perfil'),
    
]