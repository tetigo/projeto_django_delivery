from django.contrib import admin
from .models import Adicional, Categoria, Opcoes, Produto


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display=['icone', 'nome_produto', 'categoria', 'preco', 'ativo']
    list_editable=['preco', 'ativo']


admin.site.register(Adicional)
admin.site.register(Categoria)
admin.site.register(Opcoes)


