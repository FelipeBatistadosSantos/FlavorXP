from django.urls import path
from django.contrib.auth.views import LoginView
from .views import cadastro, CustomLoginView, home, host, perfil, CustomLogoutView, editar_perfil, editar_host, perfil_host

app_name = 'angeline'

urlpatterns = [
    path('cadastro', cadastro, name='cadastro'),
    path('login', CustomLoginView.as_view(), name='login'),
    path('home', home, name='home'),
    path('seja host', host, name='host'),
    path('perfil', perfil, name='perfil'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('editar_perfil', editar_perfil, name='editar_perfil'),
    path('editar_host', editar_host, name='editar_host'),
    path('perfil_host', perfil_host, name='perfil_host'),

]