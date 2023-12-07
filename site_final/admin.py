from django.contrib import admin
from .models import Categoria,SubCategoria,Servico,Perfil,SalaDeMensagens,Mensagem,DiaDaSemana,PropostaAceita,PropostaServico

admin.site.register(Categoria)
admin.site.register(SubCategoria)
admin.site.register(Servico)
admin.site.register(Perfil)
admin.site.register(SalaDeMensagens)
admin.site.register(Mensagem)
admin.site.register(DiaDaSemana)
admin.site.register(PropostaAceita)
admin.site.register(PropostaServico)