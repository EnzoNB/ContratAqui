from django.contrib import admin
from .models import Categoria,SubCategoria,Servico,Perfil,SalaDeMensagens,Mensagem

admin.site.register(Categoria)
admin.site.register(SubCategoria)
admin.site.register(Servico)
admin.site.register(Perfil)
admin.site.register(SalaDeMensagens)
admin.site.register(Mensagem)
