import csv
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myfood.settings')  
django.setup()

from angeline.models import Estado  

def popular_estados_com_csv(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo_csv:
        leitor_csv = csv.reader(arquivo_csv)
        next(leitor_csv)  

        for linha in leitor_csv:
            codigo, nome, sigla = linha
            codigo = int(codigo)

            estado = Estado.objects.create(
                codigo=codigo,
                nome=nome,
                sigla=sigla,
            )

            print(f"Estado criado: {estado.nome}")

caminho_arquivo_csv = 'angeline/static/angeline/estados.csv'
popular_estados_com_csv(caminho_arquivo_csv)
