from django.urls import path
from .views import *     #import all the functions, to run our URL Link from the file views.py   
from django.contrib.auth import views

urlpatterns = [
    path('',homepage, name='homepage'),                      #homepage
    path('loja/',loja, name='loja'),                            #store
    path('loja/<str:filtro>/',loja, name='loja'),       #store  but filtering according to product category            
    path('produto/<int:id_produto>/', ver_produto, name='ver_produto'), #dynamically, for each product, "create" a details page, all pages are the same, but we have to get the product id to show    
    path('produto/<int:id_produto>/<int:id_cor>/', ver_produto, name="ver_produto"),                               
    path('carrinho', carrinho, name='carrinho'),
    path('checkout',checkout, name='checkout' ),             #checkout
    path('adicionarcarrinho/<int:id_produto>/',adicionar_carrinho, name='adicionar_carrinho'),
    path('removercarrinho/<int:id_produto>/',remover_carrinho, name='remover_carrinho'),
    path('adicionarendereco/', adicionar_endereco, name='adicionar_endereco'),

    path('finalizarpedido/<int:id_pedido>/', finalizar_pedido, name='finalizar_pedido'),
    path('finalizar_pagamento/', finalizar_pagamento, name='finalizar_pagamento'),
    path('pedidoaprovado/<int:id_produto>/', pedido_aprovado, name='pedido_aprovado'),

    path('minhaconta/', minha_conta, name='minha_conta'),                    #my account
    path('fazerlogin/',fazer_login, name='fazer_login'),                         #login
    path('criarconta/',criar_conta, name='criar_conta'),  
    path('fazerlogout/',fazer_logout, name='fazer_logout'), 
    path('meuspedidos', meus_pedidos, name='meus_pedidos'),

    path("password_change/", views.PasswordChangeView.as_view(), name="password_change"),                   #change password
    path("password_change/done/", views.PasswordChangeDoneView.as_view(), name="password_change_done"),     #if the password was sucess changed

    path("password_reset/", views.PasswordResetView.as_view(), name="password_reset"),                      #link to reset passoword
    path("password_reset/done/", views.PasswordResetDoneView.as_view(), name="password_reset_done"),        
    path("reset/<uidb64>/<token>/", views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"), 
    path("reset/done/", views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),



]

