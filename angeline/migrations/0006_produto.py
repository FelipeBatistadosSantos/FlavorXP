# Generated by Django 5.0.1 on 2024-01-25 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('angeline', '0005_alter_customuser_cpf_alter_customuser_is_active_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('preco', models.DecimalField(decimal_places=2, max_digits=10)),
                ('categoria', models.CharField(max_length=50)),
                ('cidade', models.CharField(max_length=50)),
            ],
        ),
    ]