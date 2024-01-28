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