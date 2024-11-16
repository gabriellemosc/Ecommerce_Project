from django.shortcuts import render
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
def ver_produto(request, id_produto):       #the id product to show the unique HTML file for each product
    produto = Produto.objects.get(id=id_produto)
    itens_estoque = ItemEstoque.objects.filter(produto=produto,quantidade__gt=0)    #search for the product in our DB, that are greater than '0'
    context = {"produto": produto, 'itens_estoque': itens_estoque}
    return render(request, 'ver_produto.html', context)


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