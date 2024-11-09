from django.urls import path
from .views import *     #import all the functions, to run our URL Link from the file views.py   

urlpatterns = [
    path('',homepage, name='homepage'),                      #homepage
    path('loja/',loja, name='loja'),                              #store
    path('minhaconta/', minha_conta, name='minhaconta'),                    #my account
    path('login',login, name='login' ),                         #login
    path('carrinho', carrinho, name='carrinho'),
    path('checkout',checkout, name='checkout' ),             #checkout
]