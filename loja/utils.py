from django.db.models import Max, Min #to filter min and max price
from django.core.mail import send_mail                                                  #send email
import csv
from django.http import HttpResponse


def filtrar_produtos(produtos, filtro, preco_minimo=0, preco_maximo=1000000, tamanho=None):
    if filtro:
        if "-" in filtro:
            categoria,tipo = filtro.split('-')             #we're gonna separate in a list 
            produtos = produtos.filter(categoria__slug=categoria, tipo__slug=tipo)
        else:
            produtos = produtos.filter(categoria__slug=filtro)
    return produtos

def preco_minimo_maximo(produtos):
#start the variable with 0 to not get a error
    minimo = 0
    maximo = 0
    if len(produtos) > 0:
        maximo = list(produtos.aggregate(Max("preco")).values())[0]         #get the max price of our DB 'produtos'
        maximo = round(maximo,2)
        minimo = list(produtos.aggregate(Min("preco")).values())[0]
        minimo = round(minimo,2)
    return minimo, maximo

#order products by price and most sales

def ordenar_produtos(produtos, ordem):
    if ordem == "menor-preco":
        produtos = produtos.order_by("preco")
    elif ordem == "maior-preco":
        produtos = produtos.order_by("-preco")
    elif ordem == "mais-vendidos":
        lista_produtos = []
        for produto in produtos:
            lista_produtos.append((produto.total_vendas(), produto))
        lista_produtos = sorted(lista_produtos, reverse=True, key=lambda tupla: tupla[0])
        produtos = [item[1] for item in lista_produtos]
    
    return produtos


def enviar_email_compra(pedido):
        email = pedido.cliente.email
        assunto = f"Pedido Aprovado: {pedido.id}"
        corpo = f"""Parabéns, Seu Pedido foi Aprovado.
        ID do pedido: {pedido.id}
        Valor Total: {pedido.preco_total}"""
        remetente = "gabriel.lemos1910@gmail.com"
        send_mail(assunto,corpo,remetente,[email])

def exportar_csv(informacoes):
    colunas = informacoes.model._meta.fields
    nomes_colunas = [coluna.name for coluna in colunas]

    resposta = HttpResponse(content_type='text/csv')
    resposta['Content-Disposition'] = "attchment; filename= export.csv "
    criado_csv = csv.writer(resposta, delimiter=';')
    #write colows
    criado_csv.writerow(nomes_colunas)
    #write rows
    for linha in informacoes.values_list():
        criado_csv.writerow(linha)



    return resposta