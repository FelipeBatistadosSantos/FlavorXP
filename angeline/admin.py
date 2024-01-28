from django.contrib import admin
from .models import CustomUser, Cidade

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Cidade)