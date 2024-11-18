from django.db import models
from django.contrib.auth.models import User         #User is the DB of Django, we did not create that DB

# Create your models here.

#the table Cliente from the database
class Cliente(models.Model):                
    nome = models.CharField(max_length=200, null=True, blank=True)      # we're gonna accept a user without name, email and phone   
    email = models.CharField(max_length=200, null=True, blank=True)
    telefone = models.CharField(max_length=200, null=True, blank=True)
    id_sessao = models.CharField(max_length=200, null=True, blank=True)
    usuario = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)                                    #each user can only have one customer

    def __str__(self):
        return str(self.nome)
#category (male, female, childish)
class Categoria(models.Model):
    nome = models.CharField(max_length=200, null=True, blank=True)

    #show the name of the product, without 'object' appearing after the word
    def __str__(self):
        return str(self.nome)
    
#type (shirt, t-shirt, shorts, pants etc)
class Tipo(models.Model):           
    nome = models.CharField(max_length=200, null=True, blank=True)

    # show the name of the product, without 'object' appearing after the word
    def __str__(self):
        return str(self.nome)

#table product
class Produto(models.Model):
    imagem =  models.ImageField(null=True, blank=True)
    nome =   models.CharField(max_length=200, null=True, blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)            
    ativo = models.BooleanField(default=True)                           #by default when we create a product it will be active
    categoria = models.ForeignKey(Categoria, null=True, blank=True, on_delete=models.SET_NULL)
    tipo = models.ForeignKey(Tipo, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Nome: {self.nome}, Categoria: {self.categoria}, Tipo: {self.tipo}, Preço: {self.preco}"
    
#color of the product
class Cor(models.Model):
    nome = models.CharField(max_length=200, null=True, blank=True)
    codigo = models.CharField(max_length=200, null=True, blank=True)    

    def __str__(self):
        return str(self.nome)

#stock
class ItemEstoque(models.Model):
    produto = models.ForeignKey(Produto, null=True, blank=True, on_delete=models.SET_NULL)
    cor = models.ForeignKey(Cor, max_length=200, null=True, blank=True, on_delete=models.SET_NULL)
    tamanho = models.CharField(max_length=200, null=True, blank=True)
    quantidade = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.produto.nome}, Tamanho: {self.tamanho}, Cor: {self.cor.nome}"

#Adress

class Endereco(models.Model):
        rua = models.CharField(max_length=400, null=True, blank=True)
        numero = models.IntegerField(default=0)
        complemento = models.CharField(max_length=200, null=True, blank=True)
        cep = models.CharField(max_length=200, null=True, blank=True)
        cidade = models.CharField(max_length=200, null=True, blank=True)
        estado = models.CharField(max_length=200, null=True, blank=True)
        cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.SET_NULL)


#order
class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, null=True, blank=True, on_delete=models.SET_NULL)
    finalizado = models.BooleanField(default=False)
    codigo_transacao =  models.CharField(max_length=200, null=True, blank=True)
    endereco = models.ForeignKey(Endereco, null=True, blank=True, on_delete=models.SET_NULL)
    data_finalizacao = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Cliente: {self.cliente.email}, ID-Pedido: {self.id}, Finalizado: {self.finalizado}"


#items ordered
class ItensPedido(models.Model):
    item_estoque = models.ForeignKey(ItemEstoque, null=True, blank=True, on_delete=models.SET)
    quantidade = models.IntegerField(default=0)
    pedido = models.ForeignKey(Pedido, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"ID Pedido: {self.pedido.id}, Produto: {self.item_estoque.produto.nome}, {self.item_estoque.tamanho, {self.item_estoque.cor.nome}}"

# the banners that we use in our homepage

class Banner(models.Model):
    imagem = models.ImageField(null=True, blank=True)
    link_destino =  models.CharField(max_length=400, null=True, blank=True)
    ativo = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.link_destino} - Ativo: {self.ativo}"     #to verify if is active
    
#Whenever a user creates an account on our website, we will create an account for them
