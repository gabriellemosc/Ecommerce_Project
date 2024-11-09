from django.shortcuts import render

# Create your views here.


def homepage(request):              
    return render(request, 'homepage.html')     #load the HTML file

# store
def loja(request):              
    return render(request, 'loja.html')     #load the HTML file


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