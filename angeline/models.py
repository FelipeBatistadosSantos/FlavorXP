from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O endereço de e-mail deve ser fornecido')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser):
    nome = models.CharField(max_length=255, default=False)
    endereco = models.CharField(max_length=255, default=False)
    telefone = models.CharField(max_length=15, default=False)
    cpf = models.CharField(max_length=11, default=False, unique=True)
    cidade = models.CharField(max_length=30, default=False)
    estado = models.CharField(max_length=30, default=False)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True, default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'endereco', 'telefone', 'cidade', 'cpf', 'estado']

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def has_module_perms(self, app_label):
        return True
    
    def has_perm(self, perm, obj=None):
        return True