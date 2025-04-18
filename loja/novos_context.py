from .models import Pedido, ItensPedido,Cliente,Categoria,Tipo

#   the 'carrinho' must be accessible to all views, so we created a separate file to make this possible
def carrinho(request):
    quantidades_produtos_carrinho = 0
    if request.user.is_authenticated:
        try:
            cliente = request.user.cliente      #get the client
        except Cliente.DoesNotExist:
                cliente = None
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
    categorias_navegacao = Categoria.objects.all()
    tipos_navegacao = Tipo.objects.all()
    return{"categorias_navegacao":categorias_navegacao, "tipos_navegacao": tipos_navegacao}

def faz_parte_equipe(request):
    equipe = False
    if request.user.is_authenticated:
        if request.user.groups.filter(name="equipe").exists():
            equipe = True
    return {"equipe":equipe}




