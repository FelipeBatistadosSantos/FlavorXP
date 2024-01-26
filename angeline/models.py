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

    PROEFICIENCIA_CHOICES = [
        ('basico', 'Básico'),
        ('intermediario', 'Intermediário'),
        ('avancado', 'Avançado'),
        ('fluente', 'Fluente')
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
    proficiencia = models.CharField('Proficiência', max_length=20, choices=PROEFICIENCIA_CHOICES, default=False)
    comidaf = models.CharField('comida', max_length=50)
    bebida = models.CharField('bebida',max_length=50)
    restricao = models.CharField('restricao', choices=RESTRICAO_CHOICES, max_length=30)
    

class Estado(models.Model):
    codigo = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=50)
    sigla = models.CharField(max_length=2)
    codigoCapital = models.IntegerField()

    def __str__(self):
        return self.nome

class Cidade(models.Model):
    codigoUf = models.IntegerField()
    codigo = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=50)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

    