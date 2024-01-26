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
    cep = models.CharField('cep', max_length=15, default=False)
    cpf = models.CharField('cpf', max_length=11, default=False)
    cidade = models.CharField('cidade', max_length=50, default=False)
    estado = models.CharField('estado', max_length=2, default=False)
    telefone = models.CharField('telefone', max_length=11, default=False)
    nascimento = models.CharField('nascimento', max_length=10)
    sobre = models.TextField('sobre', default=False)
    profissao = models.CharField('profissao',max_length=50)
    hobbie = models.CharField('hobbie', max_length=50)
    idioma = models.CharField('idioma', choices=IDIOMA_CHOICES, max_length=30)
    proficiencia = models.CharField('Proficiência', max_length=20, choices=PROEFICIENCIA_CHOICES, default=False)
    comidaf = models.CharField('comidaf', max_length=50)
    bebida = models.CharField('bebida',max_length=50)
    restricao = models.CharField('restricao', choices=RESTRICAO_CHOICES, max_length=30)


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


