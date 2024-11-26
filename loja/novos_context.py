from .models import Pedido, ItensPedido,Cliente,Categoria,Tipo

#   the 'carrinho' must be accessible to all views, so we created a separate file to make this possible
def carrinho(request):
    quantidades_produtos_carrinho = 0
    if request.user.is_authenticated:
        cliente = request.user.cliente      #get the client
    else:
        if request.COOKIES.get('id_sessao'):        #get the session id 
            id_sessao = request.COOKIES.get('id_sessao')
            cliente,criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
        else:
            return{"quantidades_produtos_carrinho": quantidades_produtos_carrinho}  #return 0 
    pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False) #If no order was created, we create an empty order for the customer, otherwise we would get an error
    #how many products are in the user's order
    itens_pedido = ItensPedido.objects.filter(pedido=pedido)
    for item in itens_pedido:
        quantidades_produtos_carrinho += item.quantidade
    return{"quantidades_produtos_carrinho": quantidades_produtos_carrinho} 

def categorias_tipos(request):
    categorias = Categoria.objects.all()
    tipos = Tipo.objects.all()
    return{"categorias":categorias, "tipos": tipos}
