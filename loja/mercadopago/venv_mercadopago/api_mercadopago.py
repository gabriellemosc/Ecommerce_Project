import mercadopago

public_key = "APP_USR-85113884-99be-4368-862b-d43b58c2ff47"

token = "APP_USR-8141489178571036-121319-7bb537209b919a3669331fb192835633-2157457722"

# Adicione as credenciais
sdk = mercadopago.SDK(token)

# itens that user is buying
#final price
preference_data = {
    "items": [
        {
            "title": "My Item",
            "quantity": 1,
            "unit_price": 75.76
        }
    ],
    "back_urls": {
        "sucess": link,
        "pending": link,
        "failure": link,
    }
}

resposta = sdk.preference().create(preference_data)
link = resposta["response"]["init_point"]

id_pagamento = resposta["response"]["id"]

print(link)