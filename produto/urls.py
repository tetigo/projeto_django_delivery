from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home_url"),
    path("categoria/<int:id>/", views.categorias, name="categorias_url"),
    path("<int:id>/", views.produto, name="produto_url"),
    path("add_carrinho/", views.add_carrinho, name="add_carrinho_url"),
    path("ver_carrinho/", views.ver_carrinho, name="ver_carrinho_url"),
    path("remover_carrinho/<int:id>", views.remover_carrinho, name='remover_carrinho_url'),
]
