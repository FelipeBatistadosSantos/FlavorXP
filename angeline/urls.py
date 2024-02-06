from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.contrib.auth.views import LoginView
from .views import cadastro, CustomLoginView, home, host, perfil, CustomLogoutView, editar_perfil, editar_host, perfil_host, evento, specific_page, host_servico, agendamento, editar_evento, agendamentos, cancelar, excluir_evento

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
    path('evento', evento, name='evento'),
    path('specific_page/<int:evento_id>/', specific_page, name='specific_page'),
    path('host_servico/<int:evento_id>/', host_servico, name='host_servico'),
    path('agendamento/<int:evento_id>/', agendamento, name='agendamento'),
    path('editar_evento/<int:evento_id>/', editar_evento, name='editar_evento'),
    path('agendamentos', agendamentos, name='agendamentos'),
    path('cancelar/<int:agendamento_id>/cancelar/', cancelar, name='cancelar'),
    path('excluir_evento/<int:evento_id>/', excluir_evento, name='excluir_evento'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)