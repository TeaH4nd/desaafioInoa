from django.contrib import admin
from .models import Acao, Preco, Perfil, Salvo

#adicionando modelos para a pagina de admin
admin.site.register(Acao) 
admin.site.register(Preco) 
admin.site.register(Perfil) 
admin.site.register(Salvo) 
