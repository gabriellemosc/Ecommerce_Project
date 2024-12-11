from django.shortcuts import render, redirect
from .models import *                       #import all the tables 
import uuid         #random number
from .utils import filtrar_produtos, preco_minimo_maximo, ordenar_produtos
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email       
from django.core.exceptions import ValidationError      #to show a erro in create a account 
from datetime import datetime
# Create your views here.


def homepage(request):      
    banners = Banner.objects.filter(ativo=True)     #filter by products that are 'active', "ativo" is a boolean camp of our object
    context = {"banners": banners}    
    return render(request, 'homepage.html', context)     #load the HTML file

# store 
def loja(request, filtro=None):     #is None because we wait for the user to filter by the category 
    produtos = Produto.objects.filter(ativo=True)            #queryset
    produtos = filtrar_produtos(produtos, filtro)       #we create a separete file to organize
#if the user applied the filter to search for products
    if request.method == "POST":                        #if the user send a forms
        dados = request.POST.dict()     #info of the request
        produtos = produtos.filter(preco__gte=dados.get("preco_minimo"), preco__lte=dados.get("preco_maximo"))
        if "tamanho" in dados:
            itens = ItemEstoque.objects.filter(produto__in=produtos, tamanho=dados.get("tamanho"))      
            ids_produtos = itens.values_list("produto", flat=True).distinct()
            produtos = produtos.filter(id__in=ids_produtos)
        if "tipo" in dados:
            produtos = produtos.filter(tipo__slug=dados.get("tipo"))
        if "categoria" in dados:
            produtos = produtos.filter(categoria__slug=dados.get("categoria"))

    #max and min price
    # variable of size
    itens = ItemEstoque.objects.filter(quantidade__gt=0, produto__in=produtos)
    tamanhos = itens.values_list("tamanho", flat=True).distinct()                          #bring the distincts sizes
    ids_categorias = produtos.values_list("categoria", flat=True).distinct()
    categorias = Categoria.objects.filter(id__in=ids_categorias)

    #call the function of utils
    minimo, maximo = preco_minimo_maximo(produtos)

    ordem = request.GET.get("ordem", "menor-preco")
    produtos = ordenar_produtos(produtos,ordem)



    context = {'produtos': produtos, "minimo":minimo, "maximo":maximo, "tamanhos":tamanhos}
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
                resposta.set_cookie(key="id_sessao", value=id_sessao, max_age=60*60*24*30) #time of expire to one month
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
    if request.user.is_authenticated:
        cliente = request.user.cliente
    else:
        if request.COOKIES.get("id_sessao"):
            id_sessao =  request.COOKIES.get('id_sessao')
            cliente,criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
        else:
            return redirect('loja') 
    pedido, criado = Pedido.objects.get_or_create(cliente=cliente, finalizado=False) #If no order was created, we create an empty order for the customer, otherwise we would get an error
    enderecos = Endereco.objects.filter(cliente=cliente)
    context = {"pedido": pedido, "enderecos": enderecos, "erro":None}        
    return render(request, 'checkout.html', context)     #load the HTML file

#finalize order after checkout
def finalizar_pedido(request, id_pedido):
    erro = None
    if request.method == "POST":
         dados = request.POST.dict()
         print(dados)
         total = dados.get("total")
         pedido = Pedido.objects.get(id=id_pedido)  #we take the order we are analyzing
         if total != pedido.preco_total:            #If the total checkout price is different from the price we have in our database, an error will be generated.
             erro = "preco"
         if not "endereco" in dados:                #if there's not a address
             erro =  "endereco"
         else:
             endereco = dados.get("endereco")     
             pedido.endereco = endereco  
         if not request.user.is_authenticated:      
            email = dados.get("email")
            try:
                validate_email(email)           #If the user has not authenticated, we try to authenticate their email
            except ValidationError:
                 erro = "email"
                 if not erro:
                     clientes = Cliente.objects.filter(email=email)
                     if clientes:
                         pedido.cliente = clientes[0]
                     else:
                         pedido.cliente.email = email
                         pedido.cliente.save()
         
         codigo_transacao = f"{pedido.id}--{datetime.now().timestamp()}"
         pedido.codigo_transacao = codigo_transacao
         pedido.save()
         if erro:
             enderecos = Endereco.objects.filter(cliente=pedido.cliente)
             context = {"erro": erro, "pedido": pedido, "enderecos": enderecos}
             return render(request, "checkout.html", context)
         else:
             #TODO pagamento do usuario
             return redirect("checkout", erro)
        
    else:
        return redirect("loja")



# add adress
def adicionar_endereco(request):
    if request.method == "POST":        
        #handle form submission
        if request.user.is_authenticated:
             cliente = request.user.cliente
        else:
            if request.COOKIES.get("id_sessao"):
                id_sessao =  request.COOKIES.get('id_sessao')
                cliente,criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
            else:
                 return redirect('loja') 
        dados = request.POST.dict()     #get the info about the requisition
        endereco = Endereco.objects.create(cliente=cliente, rua=dados.get('rua'),numero=int(dados.get('numero')),estado=dados.get('estado'),cidade=dados.get('cidade'),cep=dados.get('cep'), complemento=dados.get('complemento'))
        endereco.save()
        return redirect('checkout')
    else:
        context = {}
        return render(request, 'adicionar_endereco.html', context)

# Page My account
@login_required
def minha_conta(request):   
    erro = None
    alterado = False
    if request.method == "POST":
        dados = request.POST.dict()
        if "senha_atual" in dados:
            #changing the password
            senha_atual = dados.get("senha_atual")
            nova_senha = dados.get("nova_senha")
            nova_senha_confirmacao = dados.get("nova_senha_confirmacao")
            if nova_senha == nova_senha_confirmacao:
                #verify if the actual password is correct
                 usuario = authenticate(request,username=request.user.email, password=senha_atual) 
                 if usuario:        #password is correct
                        usuario.set_password(nova_senha)
                        usuario.save()
                        alterado = True
                 else:
                     erro = "senha_incorreta"
            else:
                erro = "senhas_diferentes"
        elif "email" in dados:
           email = dados.get("email") 
           telefone = dados.get("telefone")
           nome = dados.get("nome")
           if email != request.user.email:          #trying to change the email
               #we cant allow the user change the email for any that already exist in our DB
               usuario = User.objects.filter(email=email)
               if len(usuario) > 0:     #if there's a user with this email
                   erro = " email_existente"
           if not erro:
                cliente = request.user.cliente
                cliente.email = email
                request.user.email = email
                request.user.username = email
                cliente.nome = nome
                cliente.telefone = telefone
                cliente.save()
                request.user.save()
                alterado = True

        else:
            erro = "formulario_invalido"
            #changing info         
    context = {"erro": erro, "alterado":alterado}
    return render(request, 'usuario/minha_conta.html', context)     #load the HTML file

#order 
@login_required
def meus_pedidos(request):
    cliente = request.user.cliente
    pedidos = Pedido.objects.filter(finalizado=True,cliente=cliente).order_by("-data_finalizacao")

    context = {"pedidos": pedidos}
    return render(request, "usuario/meus_pedidos.html", context)

#login page
def fazer_login(request): 
    erro = False  
    if request.user.is_authenticated:   #if user is already authenticated we redirect him to the store
        return redirect('loja')      
    if request.method == "POST":
        dados = request.POST.dict() 
        if 'email' in dados and 'senha' in dados:           # if the post has email and password
            email = dados.get('email')
            senha = dados.get('senha')
            usuario = authenticate(request,username=email, password=senha)        
            if usuario:     #if there's a user
                #make login
                login(request, usuario)
                return redirect('loja')
            else:
                erro = True                        #we will label the types of errors, so that the html shows different types of errors
        else:
            erro = True
    context = {"erro":erro}
    return render(request, 'usuario/login.html', context)     #load the HTML file


#create a account

def criar_conta(request):
    erro = None
    if request.user.is_authenticated:
        return redirect('loja')
    if request.method == "POST":
        dados = request.POST.dict()
        if "email" in dados and "senha" in dados and "confirmacao_senha" in dados:
            #create account
            email = dados.get("email")
            senha = dados.get("senha")
            confirmacao_senha = dados.get("confirmacao_senha")
            try:
                validate_email(email)
            except ValidationError:
                erro = "email_invalido"
            if senha == confirmacao_senha:
                #create account
                usuario, criado = User.objects.get_or_create(username=email, email=email)        #verify if there's a user, if positive create one
                if not criado:                                                     #means that the user already exists
                    erro = "usuario_existente"
                else:                                                               #if the user was create
                    usuario.set_password(senha)
                    usuario.save()
                    #make login
                    usuario = authenticate(request, username=email, password=senha)
                    login(request, usuario)
                    
                    #checks if there are id cookies in the browser
                    if request.COOKIES.get("id_sessao"):
                        id_sessao =  request.COOKIES.get('id_sessao')
                        cliente,criado = Cliente.objects.get_or_create(id_sessao=id_sessao)
                    else:
                        cliente,criado = Cliente.objects.get_or_create(usuario=usuario, defaults={"email":email})
                    cliente.usuario = usuario
                    cliente.email = email
                    cliente.save()
                    return redirect('loja')
            else:
                erro = "senhas_diferentes"
        else:
            erro = "preenchimento"
    context = {"erro":erro}
    return render(request, "usuario/criarconta.html", context)


#logout
@login_required
def fazer_logout(request):
    logout(request)
    return redirect("fazer_login")