from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('home.html', views.home, name="home"),
    path('portifolio.html', views.portifolio, name="portifolio"),
    path('delete/<acao_id>', views.delete, name="delete"),
    path('atualizar', views.atualizar, name="atualizar"),
    path('<acao_id>', views.acao  , name="acao"),

]
