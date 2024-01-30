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

        for linha in sorted(leitor_csv, key=lambda x: x[2]):  # Ordena pelo terceiro elemento
            codigo_uf, codigo_ibge, nome = linha

            estado, created = Estado.objects.get_or_create(codigo=int(codigo_uf), defaults={'nome': 'Unknown', 'sigla': 'XX'})
            
            cidade, created = Cidade.objects.get_or_create(
                codigo_uf=int(codigo_uf),
                codigo_ibge=int(codigo_ibge),
                defaults={
                    'nome': nome,
                    'estado': estado,
                }
            )

            print(f"Cidade criada: {cidade.nome}")

caminho_arquivo_csv_cidades = 'angeline/static/angeline/municipios.csv'
popular_cidades_com_csv(caminho_arquivo_csv_cidades)
