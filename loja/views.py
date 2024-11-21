from django.shortcuts import render, redirect
from .models import *                       #import all the tables 
import uuid         #random number
# Create your views here.


def homepage(request):      
    banners = Banner.objects.filter(ativo=True)     #filter by products that are 'active', "ativo" is a boolean camp of our object
    context = {"banners": banners}    
    return render(request, 'homepage.html', context)     #load the HTML file

# store
def loja(request, nome_categoria=None):     #is None because we wait for the user to filter by the category 
    produtos = Produto.objects.filter(ativo=True)            #queryset
    if nome_categoria:
        produtos = produtos.filter(categoria__nome=nome_categoria)          
    context = {'produtos': produtos}
    return render(request, 'loja.html', context)     #load the HTML file

# see the details of the product
def ver_produto(request, id_produto, id_cor=None):
    tem_estoque = False
    cores = set()
    tamanhos = []
    cor_selecionada = None
    if id_cor:
        cor_selecionada = Cor.objects.get(id=id_cor)
    # serach the product by the id
    produto = Produto.objects.get(id=id_produto)

    # search itens with more than 
    itens_estoque = ItemEstoque.objects.filter(produto=produto, quantidade__gt=0)

    # if there is item, then define the color
    if itens_estoque.exists():
        tem_estoque = True
        cores = {item.cor for item in itens_estoque}  # assure unique values

        #  filter by color, if a color id was send
        if id_cor:
            itens_estoque = itens_estoque.filter(cor__id=id_cor)
        
        # Extract unique sizes for remaining items
        tamanhos = list(itens_estoque.values_list('tamanho', flat=True))
    
   

    # Cria o contexto para o template
    context = {
        "produto": produto,
        "itens_estoque": itens_estoque,
        "tem_estoque": tem_estoque,
        "cores": cores,
        "tamanhos": tamanhos,
        "cor_selecionada": cor_selecionada
    }

    return render(request, 'ver_produto.html', context)

# add product to buy
def adicionar_carrinho(request, id_produto):
    if request.method == "POST" and id_produto:
        dados = request.POST.dict()                 #get info of the request
        tamanho = dados.get('tamanho')
        id_cor = dados.get('cor')
        print(dados)
        if not tamanho:
            return redirect('loja')
        resposta = redirect('carrinho')
        #get the client
        if request.user.is_authenticated:
            cliente = request.user.cliente
        else:
            #we will store the customer session data
            if request.COOKIES.get('id_sessao'):                #we check if the user already has a session id
                id_sessao =  request.COOKIES.get('id_sessao')       #we get the session id
            else:
                id_sessao = str(uuid.uuid4())               #random session number that we create if the user doesn't have one
                resposta.set_cookie(key="id_sessao", value=id_sessao)
            cliente, criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
        pedido,criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
        item_estoque = ItemEstoque.objects.get(produto__id=id_produto, tamanho=tamanho, cor__id=id_cor)
        item_pedido, criado = ItensPedido.objects.get_or_create(item_estoque=item_estoque, pedido=pedido)
        item_pedido.quantidade += 1
        item_pedido.save()      # we need to save in our DB, cuz we modified the order
        return resposta
        #create the order or pick up the order that is open
    else:
        return redirect('loja')
    
def remover_carrinho(request, id_produto):
     if request.method == "POST" and id_produto:
        dados = request.POST.dict()                 #get info of the request
        tamanho = dados.get('tamanho')
        id_cor = dados.get('cor')
        if not tamanho:
            return redirect('loja')
        #get the client
        if request.user.is_authenticated:
            cliente = request.user.cliente
        else:
            if request.COOKIES.get('id_sessao'):
                id_sessao = request.COOKIES.get('id_sessao')
                cliente,criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
            else:
                return redirect('loja')
        pedido,criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False)
        item_estoque = ItemEstoque.objects.get(produto__id=id_produto, tamanho=tamanho, cor__id=id_cor)
        item_pedido, criado = ItensPedido.objects.get_or_create(item_estoque=item_estoque, pedido=pedido)
        item_pedido.quantidade -= 1
        item_pedido.save()      # we need to save in our DB, cuz we modified the order
        if item_pedido.quantidade <= 0:         
            item_pedido.delete()
        return redirect('carrinho')
     
        #create the order or pick up the order that is open
     else:
        return redirect('loja')



#verify and see the 'carrinho'
def carrinho(request):    
    if request.user.is_authenticated:
        cliente = request.user.cliente
    else:
        if request.COOKIES.get("id_sessao"):
            id_sessao =  request.COOKIES.get('id_sessao')
            cliente,criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
        else:
            context = {"cliente_existente":False,"itens_pedido":None, "pedido": None}       #we send the variables for to be sure will not show any error
            return render(request, 'carrinho.html', context) 
    pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False) #If no order was created, we create an empty order for the customer, otherwise we would get an error
    #how many products are in the user's order
    itens_pedido = ItensPedido.objects.filter(pedido=pedido)  
    context = {"itens_pedido":itens_pedido, "pedido": pedido, "cliente_existente":True}        
    return render(request, 'carrinho.html', context)     #load the HTML file

#exit the site
def checkout(request):              
    return render(request, 'checkout.html')     #load the HTML file

# Page My account
def minha_conta(request):              
    return render(request, 'usuario/minha_conta.html')     #load the HTML file
#login page
def login(request):              
    return render(request, 'usuario/login.html')     #load the HTML file