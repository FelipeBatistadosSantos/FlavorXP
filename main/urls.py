from django.urls import path
from .views import base
app_name = 'main'

urlpatterns = [
    path('', base, name='base')
]