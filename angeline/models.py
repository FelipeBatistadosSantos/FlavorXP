from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, User
from django.db import models
from django.utils import timezone
from localflavor.br.models import BRPostalCodeField, BRCPFField
from phonenumber_field.modelfields import PhoneNumberField



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
    

class Estado(models.Model):
    codigo = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=50)
    sigla = models.CharField(max_length=2)
    
    def __str__(self):
        return self.nome


class Cidade(models.Model):
    codigo_uf = models.IntegerField()
    codigo_ibge = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=50)
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE, default='')

    def __str__(self):
        return self.nome

    
class CompleteCadastro(models.Model):

    IDIOMA_CHOICES = [
        ('nenhuma', 'Nenhum'),
        ('ingles', 'Inglês'),
        ('espanhol', 'Espanhol'),
        ('italiano', 'Italiano'),
        ('alemão', 'Alemão'),
        ('outro', 'Outro')
    ]

    RESTRICAO_CHOICES = [
        ('nenhum', 'Nenhum'),
        ('gluten', 'Glúten'),
        ('lactose', 'Lactose'),
        ('vegano', 'Vegano'),
        ('vegetariano', 'Vegetariano'),
        ('outros', 'Outros')
    ]

    usuario = models.OneToOneField(User, on_delete=models.CASCADE, default='')
    cep = BRPostalCodeField()
    cpf = BRCPFField()
    cidade = models.ForeignKey(Cidade, on_delete=models.SET_NULL, null=True, blank=True)
    estado = models.ForeignKey(Estado, on_delete=models.SET_NULL, null=True, blank=True)
    telefone = PhoneNumberField(unique=True, null=False, blank=False)
    nascimento = models.DateField(null=True)
    sobre = models.TextField('sobre', default='')
    profissao = models.CharField('profissao',max_length=50)
    hobbie = models.CharField('hobbie', max_length=50)
    idioma = models.CharField('idioma', choices=IDIOMA_CHOICES, max_length=30)
    comidaf = models.CharField('comida', max_length=50)
    bebida = models.CharField('bebida',max_length=50)
    restricao = models.CharField('restricao', choices=RESTRICAO_CHOICES, max_length=30)
    outra_restricao = models.CharField('outra_restricao', max_length=30, default='')


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

    def __str__(self):
        return self.nome_empresa 


class Evento(models.Model):

    def default_data():
        return timezone.now().date()

    def default_horario():
        return timezone.now().time()

    ESTILO_CHOICES = [
            ('janta', 'Janta'),
            ('almoco', 'Almoço'),
            ('city_tour_gastronomico', 'City Tour Gastronômico'),
            ('harmonizacao', 'Harmonização'),
            ('workshop_gastronomico', 'Workshop Gastronômico'),
            ('aula_pratica', 'Aula prática de Cozinha'),
            ('outro', 'Outro'),
        ]

    id = models.AutoField(primary_key=True)
    estilo = models.CharField('Estilo de Evento', max_length=30, choices=ESTILO_CHOICES, default='')
    tema = models.CharField('Tema da experiência', max_length=255, default='Sem tema')
    fotos = models.ImageField('Fotos do Evento', upload_to='media/', blank=True, null=True, max_length=255)
    host = models.ForeignKey(Host, on_delete=models.PROTECT, default='')
    descricao = models.TextField('Descrição da experiência')
    cardapio = models.TextField('Cardápio', blank=True, null=True)
    inclui_bebidas = models.BooleanField('Inclui Bebidas?', default=False)
    bebidas_oferecidas = models.CharField('Bebidas Oferecidas', max_length=255, blank=True, null=True)
    convidado_pode_trazer = models.BooleanField('Convidado pode trazer bebidas?', default=False)
    max_convidados = models.PositiveIntegerField('Máximo de Convidados', default=1)
    local = models.CharField('Local', max_length=255, default='Minha casa')
    data = models.DateField('Data', default=default_data)
    horario = models.TimeField('Horário', default=default_horario)
    valor_host = models.DecimalField('Valor Host', max_digits=10, decimal_places=2, default=10.0)
    valor_manutencao_site = models.DecimalField('Valor Manutenção do Site (%)', max_digits=5, decimal_places=2, default=0)
    vagas_disponiveis = models.PositiveIntegerField('Vagas Disponíveis', editable=False, default=0)

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.vagas_disponiveis = self.max_convidados
        super().save(*args, **kwargs)

    def valor_total_evento(self):
        return self.valor_host + (self.valor_host * (self.valor_manutencao_site / 100))

    def __str__(self):
        return f'{self.estilo} - {self.tema} por {self.host.nome_empresa} em {self.local} em {self.data} às {self.horario}'
    

class Agendamento(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE)
    quantidade_pessoas = models.PositiveIntegerField()
    nomes_convidados = models.CharField(blank=True, null=True, max_length=100)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def save(self, *args, **kwargs):
        evento = self.evento
        if evento:
            evento.vagas_disponiveis -= self.quantidade_pessoas
            evento.save()
        super().save(*args, **kwargs)

    def calcular_valor_total(self):
        if self.evento:
            return self.evento.valor_host * self.quantidade_pessoas
        return 0

    def save(self, *args, **kwargs):
        self.valor_total = self.calcular_valor_total()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.usuario.username} - {self.evento.tema} - {self.quantidade_pessoas} pessoas'