# Generated by Django 4.2.6 on 2024-01-18 17:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('angeline', '0002_customuser_cidade'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='cpf',
            field=models.IntegerField(default=False, max_length=11),
        ),
        migrations.AddField(
            model_name='customuser',
            name='estado',
            field=models.CharField(default=False, max_length=30),
        ),
    ]