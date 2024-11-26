
def filtrar_produtos(produtos, filtro):
    if filtro:
        if "-" in filtro:
            categoria,tipo = filtro.split('-')             #we're gonna separate in a list 
            produtos = produtos.filter(categoria__slug=categoria, tipo__slug=tipo)
        else:
            produtos = produtos.filter(categoria__slug=filtro)
    return produtos