# Generated by Django 5.0.1 on 2024-01-31 18:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('angeline', '0009_alter_evento_host'),
    ]

    operations = [
        migrations.RenameField(
            model_name='completecadastro',
            old_name='descricao',
            new_name='outra_restricao',
        ),
    ]