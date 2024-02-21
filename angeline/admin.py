from django.contrib import admin

# Register your models here.


from .models import CustomUser, Host, Cidade, Estado, Evento, CompleteCadastro


# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Host)
admin.site.register(Cidade)
admin.site.register(Estado)
admin.site.register(Evento)
admin.site.register(CompleteCadastro)
