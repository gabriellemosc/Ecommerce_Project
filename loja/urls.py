from django.urls import path
from .views import *     #import all the functions, to run our URL Link from the file views.py   

urlpatterns = [
    path('',homepage, name='homepage'),                      #homepage
    path('loja/',loja, name='loja'),                            #store
    path('loja/<str:nome_categoria>/',loja, name='loja'),       #store  but filtering according to product category            
    path('produto/<int:id_produto>/', ver_produto, name='ver_produto'), #dynamically, for each product, "create" a details page, all pages are the same, but we have to get the product id to show    
    path('produto/<int:id_produto>/<int:id_cor>/', ver_produto, name="ver_produto"),                               
    path('minhaconta/', minha_conta, name='minhaconta'),                    #my account
    path('login',login, name='login'),                         #login
    path('carrinho', carrinho, name='carrinho'),
    path('checkout',checkout, name='checkout' ),             #checkout
    path('adicionarcarrinho/<int:id_produto>/',adicionar_carrinho, name='adicionar_carrinho'),
    path('removercarrinho/<int:id_produto>/',remover_carrinho, name='remover_carrinho'),
]