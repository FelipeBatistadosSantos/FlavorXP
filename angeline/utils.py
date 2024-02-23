# def filtro_evento(evento, filtro):
#     resultados = []

#     for cidade in evento:
#         for chave, dados in evento.items():
#             nome_estilo = dados.get('nome', '').lower()
#             nome_tema = dados.get('evento', '').lower()
#             nome_local = dados.get('nacionalidade', '').lower()

#             # Filtrar pelo nome da cidade, evento e nacionalidade
#             if (filtro.lower() in nome_estilo or filtro.lower() in nome_tema or filtro.lower() in nome_local) and len(filtro) > 2:
#                 resultados.append(dados)

#     return resultados