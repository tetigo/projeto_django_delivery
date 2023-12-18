from django.urls import path
from . import views

urlpatterns = [
    path("finalizar_pedido", views.finalizar_pedido, name="finalizar_pedido_url"),
    path("validar_cupom", views.validar_cupom, name="validar_cupom_url"),
]
