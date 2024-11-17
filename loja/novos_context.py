#the 'carrinho' must be accessible to all views, so we created a separate file to make this possible
def carrinho(request):
    quantidades_produtos_carrinho = 15
    return{"quantidades_produtos_carrinho": quantidades_produtos_carrinho} 