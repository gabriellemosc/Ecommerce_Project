import mercadopago
# to hide the public key and token
from decouple import config

public_key = config("PUBLIC_KEY")

token = config("TOKEN")

# Adicione as credenciais

def criar_pagamento(itens_pedido, link):
    sdk = mercadopago.SDK(token)

    # itens that user is buying
    #final price
    itens = []
    for item in itens_pedido:
        quantidade = int(item.quantidade)
        nome_produto = item.item_estoque.produto.nome
        preco_unitario =  float(item.item_estoque.produto.preco)
        itens.append({
            "title": nome_produto,
            "quantity": quantidade,
            "unit_price": preco_unitario,
        })

    preference_data = {
        "items": itens,
        "auto_return": "all",
        "back_urls": {
            "success": link,
            "pending": link,
            "failure": link,
        }
    }

    resposta = sdk.preference().create(preference_data)

    print("Resposta", resposta)
    
    link_pagamento = resposta["response"]["init_point"]

    id_pagamento = resposta["response"]["id"]

    return link_pagamento, id_pagamento