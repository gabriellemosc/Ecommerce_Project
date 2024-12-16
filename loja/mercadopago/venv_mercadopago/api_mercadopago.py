import mercadopago

public_key = "APP_USR-85113884-99be-4368-862b-d43b58c2ff47"

token = "APP_USR-8141489178571036-121319-7bb537209b919a3669331fb192835633-2157457722"

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
            "sucess": link,
            "pending": link,
            "failure": link,
        }
    }

    resposta = sdk.preference().create(preference_data)
    link_pagamento = resposta["response"]["init_point"]

    id_pagamento = resposta["response"]["id"]

    return link_pagamento, id_pagamento