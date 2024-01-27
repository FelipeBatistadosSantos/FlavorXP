# def filtrar_cidades(cidades, filtro):
#     resultados = []

#     for cidade in cidades:
#         for chave, dados in cidade.items():
#             nome_cidade = dados.get('nome', '').lower()
#             if filtro.lower() in nome_cidade:
#                 resultados.append(dados)

#     return resultados


# def filtrar_cidades(cidades, filtro, evento=None, nacionalidade=None):
#     resultados = []

#     for cidade in cidades:
#         for chave, dados in cidade.items():
#             nome_cidade = dados.get('nome', '').lower()
#             nome_evento = dados.get('evento', '').lower()  # Substitua 'evento' pelo campo correto no seu modelo
#             nome_nacionalidade = dados.get('nacionalidade', '').lower()  # Substitua 'nacionalidade' pelo campo correto no seu modelo

#             # Filtrar pelo nome da cidade, evento e nacionalidade
#             if (
#                 filtro.lower() in nome_cidade and
#                 (evento is None or evento.lower() == nome_evento) and
#                 (nacionalidade is None or nacionalidade.lower() == nome_nacionalidade)
#             ):
#                 resultados.append(dados)

#     return resultados


def filtrar_cidades(cidades, filtro):
    resultados = []

    for cidade in cidades:
        for chave, dados in cidade.items():
            nome_cidade = dados.get('nome', '').lower()
            nome_evento = dados.get('evento', '').lower()
            nome_nacionalidade = dados.get('nacionalidade', '').lower()

            # Filtrar pelo nome da cidade, evento e nacionalidade
            if (filtro.lower() in nome_cidade or filtro.lower() in nome_evento or filtro.lower() in nome_nacionalidade) and len(filtro) > 2:
                resultados.append(dados)

    return resultados

