import csv
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myfood.settings')
django.setup()

from angeline.models import Cidade, Estado

def popular_cidades_com_csv(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo_csv:
        leitor_csv = csv.reader(arquivo_csv)
        next(leitor_csv)

        for linha in leitor_csv:
            codigo_ibge, nome, latitude, longitude, capital, codigo_uf, siafi_id, ddd, fuso_horario = linha

            estado, created = Estado.objects.get_or_create(codigo=int(codigo_uf), defaults={'nome': 'Unknown', 'sigla': 'XX'})
            
            cidade = Cidade.objects.create(
                codigo=int(codigo_ibge),
                nome=nome,
                estado=estado,
                latitude=float(latitude),
                longitude=float(longitude),
                capital=bool(int(capital)),
                codigo_uf=int(codigo_uf),
            )

            print(f"Cidade criada: {cidade.nome}")

caminho_arquivo_csv_cidades = 'angeline/static/angeline/municipios.csv'
popular_cidades_com_csv(caminho_arquivo_csv_cidades)
