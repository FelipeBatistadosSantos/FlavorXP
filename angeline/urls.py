
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path
from django.contrib.auth.views import LoginView
from .views import cadastro, CustomLoginView, home, host, perfil, CustomLogoutView, editar_perfil, editar_host, perfil_host, evento, specific_page, host_servico, agendamento, editar_evento, agendamentos, cancelar, excluir_evento, completar_perfil, criar_host

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
    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset.html'), name='password_reset'),
    path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),
    path('criar_host', criar_host, name='criar_host'),
    path('completar_perfil', completar_perfil, name='completar_perfil')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)