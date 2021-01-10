from django.urls import path
from . import views

urlpatterns = [
    path('index.html', views.index, name="index"),
    path('home.html', views.home, name="home"),
    path('', views.portifolio, name="portifolio"),
    path('delete/<acao_id>', views.delete, name="delete"),
    path('deleteEmail/<email_id>', views.deleteEmail, name="deleteEmail"),
    path('atualizar', views.atualizar, name="atualizar"),
    path('preco/<acao_id>', views.acao  , name="acao"),
    path('start', views.start_get_precos  , name="start"),
    path('stop', views.stop_get_precos  , name="stop"),
    path('perfil.html', views.perfil  , name="perfil"),

]