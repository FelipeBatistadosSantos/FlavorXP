from django.urls import path
from .views import cadastro, login, home

app_name = 'angeline'

urlpatterns = [
    path('cadastro', cadastro, name='cadastro'),
    path('login', login, name='login'),
    path('home', home, name='home')
]