from django.shortcuts import render, redirect
from .models import *                       #import all the tables 
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
    
    # Prints para depuração
    print(f"Itens no estoque: {itens_estoque}")
    print(f"Produto disponível: {produto.nome}")
    print(f"Tamanhos disponíveis: {tamanhos}")

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
        print(dados)
        tamanho = dados.get('tamanho')
        id_cor = dados.get('cor')
        return redirect('carrinho')
        if not tamanho:
            return redirect('carrinho')
        #get the client
        #create the order or pick up the order that is open
    else:
        return redirect('loja')



def carrinho(request):              
    return render(request, 'carrinho.html')     #load the HTML file

#exit the site
def checkout(request):              
    return render(request, 'checkout.html')     #load the HTML file

# Page My account
def minha_conta(request):              
    return render(request, 'usuario/minha_conta.html')     #load the HTML file
#login page
def login(request):              
    return render(request, 'usuario/login.html')     #load the HTML file