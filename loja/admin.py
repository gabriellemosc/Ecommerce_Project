from django.contrib import admin
from .models import * 
# Register your models here.

# add to our ADMIN SESSION the table that we create 
admin.site.register(Cliente)
admin.site.register(Categoria)
admin.site.register(Tipo)
admin.site.register(Produto)
admin.site.register(ItemEstoque)
admin.site.register(Endereco)
admin.site.register(Pedido)
admin.site.register(ItensPedido)