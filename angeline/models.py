from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, User
from django.db import models
from cpf_field.models import CPFField


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password):
        if not email:
            raise ValueError('O endereço de e-mail deve ser fornecido')
        
        if not password:
            raise ValueError('A senha deve ser fornecida')

        email = self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    password = models.TextField(verbose_name='password')

    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    
class CompleteCadastro(models.Model):

    IDIOMA_CHOICES = [
        ('ingles', 'Inglês'),
        ('espanhol', 'Espanhol'),
        ('italiano', 'Italiano'),
        ('alemão', 'Alemão'),
        ('outro', 'Outro')
    ]

    RESTRICAO_CHOICES = [
        ('gluten', 'Glúten'),
        ('lactose', 'Lactose'),
        ('vegano', 'Vegano'),
        ('vegetariano', 'Vegetariano'),
        ('outros', 'Outros')
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE, default='')
    cep = models.CharField('cep', max_length=15, default='')
    cpf = CPFField('cpf')
    cidade = models.CharField('cidade', max_length=50, default='')
    estado = models.CharField('estado', max_length=2, default='')
    telefone = models.CharField('telefone', max_length=11, default='')
    nascimento = models.CharField('nascimento', max_length=10)
    sobre = models.TextField('sobre', default='')
    profissao = models.CharField('profissao',max_length=50)
    hobbie = models.CharField('hobbie', max_length=50)
    idioma = models.CharField('idioma', choices=IDIOMA_CHOICES, max_length=30)
    comidaf = models.CharField('comida', max_length=50)
    bebida = models.CharField('bebida',max_length=50)
    restricao = models.CharField('restricao', choices=RESTRICAO_CHOICES, max_length=30)
    

class Estado(models.Model):
    codigo = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50)
    sigla = models.CharField(max_length=2)

    def __str__(self):
        return self.nome

class Cidade(models.Model):
    codigo = models.IntegerField(primary_key=True)  
    nome = models.CharField(max_length=50)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)
    capital = models.BooleanField(default=False)
    codigo_uf = models.IntegerField(default=0)

    def __str__(self):
        return self.nome


class Host(models.Model):
    PROFISSIONAL = 'profissional'
    AMADOR = 'amador'
    AREA_GASTRONOMIA_CHOICES = [
        (PROFISSIONAL, 'Profissional'),
        (AMADOR, 'Amante da Gastronomia'),
    ]

    FREQUENCIA_CHOICES = [
        ('diaria', 'Diariamente'),
        ('semanal', 'Semanalmente'),
        ('mensal', 'Mensalmente'),
        ('ocasional', 'Ocasionalmente'),
    ]
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, default='')
    nome_empresa = models.CharField('Nome da Empresa/Marca/Apelido', max_length=100)
    motivo = models.TextField('Motivo para ser um host')
    area_gastronomia = models.CharField('Profissional da Área ou Amante da Gastronomia', max_length=20, choices=AREA_GASTRONOMIA_CHOICES)
    servicos = models.TextField('Serviços Disponíveis')
    frequencia_servicos = models.CharField('Frequência de Disponibilização de Serviços', max_length=20, choices=FREQUENCIA_CHOICES)
    local_servico = models.CharField('Local de Serviço', max_length=100)
    descricao_local = models.TextField('Descrição do Local de Serviço')


class Evento(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, default='')
    nome = models.CharField('nome', max_length=100)
    descricao = models.CharField('descricao', max_length=200)